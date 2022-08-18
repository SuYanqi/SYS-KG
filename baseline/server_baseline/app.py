import logging
from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS

from bug_finding.utils.file_util import FileUtil
from bug_finding.utils.graph_util import GraphUtil
from config import DATA_DIR
from bug_finding.utils.nlp_util import NLPUtil
from sentence_transformers import util

# configuration
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})

BUGS_EMBEDDINGS = None

def generate_text_list(bug_list, only_summary=False):
    bug_text_list = []
    for bug in bug_list:
        if only_summary:
            bug_text = bug.summary
        else:
            bug_text = bug.summary + ".\n" + bug.description.text
            # print(bug_text)
        bug_text_list.append(bug_text)
    return bug_text_list


def get_query_bug_text(bug, only_summary=False):
    if only_summary:
        bug_text = bug.summary
    else:
        bug_text = bug.summary + ".\n" + bug.description.text
        # print(bug_text)
    return bug_text


def search_top_k_bugs(bug, bugs, top_k=51, use_cuda=True):
    if use_cuda:
        device = "cuda"
    else:
        device = "cpu"

    # corpus = generate_text_list(bugs)
    # embedder = SentenceTransformer(model)
    query = [get_query_bug_text(bug)]

    # corpus_embeddings = NLPUtil.SBERT_MODEL.encode(corpus, convert_to_tensor=True).to(device)
    query_embedding = NLPUtil.SBERT_MODEL.encode(query, convert_to_tensor=True).to(device)
    hits = util.semantic_search(query_embedding, BUGS_EMBEDDINGS, top_k=top_k)
    # print(bug)
    searched_bug_list = []
    for hit in hits[0]:
        hit_id = hit["corpus_id"]
        result_bug = bugs.bugs[hit_id]
        # print(bug)
        # print(result_bug)
        if result_bug.id != bug.id:
            result_bug = get_bug_dict(result_bug)
            result_bug['Score'] = format(float(hit["score"]), '.3f')  # keep 
            searched_bug_list.append(result_bug)
    
    return searched_bug_list


def get_bug_dict(bug):
    """
    get bug dict
    @param bug:
    @type Bug:
    @return:
    @rtype:
    """
    bug_dict = {
        'id': None,
        'product': None,
        'component': None,
        'Summary': None,
        'Description': None,
        'Attachments': None,
        'Score': None,
    }
    if bug.id:
        bug_dict['id'] = bug.id
    if bug.product_component_pair.product:
        bug_dict['product'] = bug.product_component_pair.product
    if bug.product_component_pair.component:
        bug_dict['component'] = bug.product_component_pair.component
    if bug.summary:
        bug_dict['Summary'] = bug.summary
    if bug.description.text:
        bug_dict['Description'] = bug.description.text
    if bug.attachments:
                bug_dict['Attachments'] = []
                for attachment in bug.attachments:
                    attachment_dict = {
                        "file_name": attachment.file_name,
                        "type": attachment.content_type.split("/")[0],
                        "content_type": attachment.content_type,
                        "attachment_url": attachment.url,
                    }
                    if attachment_dict["type"] == "video" or attachment_dict["type"] == "image":
                        bug_dict['Attachments'].append(attachment_dict)
    return bug_dict


@app.route("/", methods=['GET', 'POST'])
def search():
    search_result = {
        'bugReport': None,
        'relevantBugReports': None,
        # 'exploratoryTestResults': None,

    }
    # data = {'name': 'nabin khadka'}
    # get input from search box
    post_data = request.get_json()
    if 'input' in post_data.keys():
        search_input = post_data['input']
        print(search_input)
        # find input_bug
        input_bug = None
        if int(search_input) in GraphUtil.BUG_ID_BUG_DICT.keys():
            input_bug = GraphUtil.BUG_ID_BUG_DICT[int(search_input)]
        # for bug in bugs:
        #     if bug.id == int(search_input):
        #         input_bug = bug
        #         break
        if input_bug:
            input_bug_dict = get_bug_dict(input_bug)
            search_result['bugReport'] = input_bug_dict
            # print(search_result)
            # print(input_bug)
            # print(bugs.bugs[0])
            relevant_bug_dict_list = search_top_k_bugs(input_bug, bugs)

            search_result['relevantBugReports'] = relevant_bug_dict_list
            
            return jsonify(search_result)
    return jsonify("")


if __name__ == "__main__":
    logging.warning("Loading SBERT model...")
    NLPUtil.load_sbert_model()
    logging.warning("Loading bugs...")
    bugs = FileUtil.load_pickle(Path(DATA_DIR, "bugs_with_step_object.json"))
    GraphUtil.get_bug_id_bug_dict(bugs)
    corpus = generate_text_list(bugs)
    BUGS_EMBEDDINGS = NLPUtil.SBERT_MODEL.encode(corpus, convert_to_tensor=True).to("cuda")
   
    logging.warning("Start the web server...")
    app.run(host='0.0.0.0', port=8091)
