import logging
from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS

from bug_finding.utils.file_util import FileUtil
from bug_finding.utils.graph_util import GraphUtil
from config import DATA_DIR

# configuration
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})


# def get_step_dict(step):
#     """
#     get step dict
#     @param step: (cluster_index, step_text, [(bugid, stepid, expected results, Actual results),...])
#     @type step: tuple
#     @return: step_dict
#     @rtype: dict
#     """
#     expected_actual_result_list = step[2]
#     expected_actual_result_dict_list = list()
#
#     for expected_actual_result in expected_actual_result_list:
#         expected_actual_result_dict = {
#             'BugId': expected_actual_result[0],
#             'StepId': expected_actual_result[1],
#             'Expected Results': expected_actual_result[2],
#             'Actual Results': expected_actual_result[3]
#         }
#         expected_actual_result_dict_list.append(expected_actual_result_dict)
#     step_dict = {
#         'ClusterIndex': step[0],
#         'StepText': step[1],
#         'ExpectedActualResultsDictList': expected_actual_result_dict_list,
#     }
#     return step_dict
#
#
# def get_bug_dict(bug):
#     """
#     get bug dict
#     @param bug:
#     @type bug:
#     @return:
#     @rtype:
#     """
#     bug_dict = {
#         'id': None,
#         'Summary': None,
#         'Preconditions': None,
#         'Steps to Reproduce': None,
#         'Expected Results': None,
#         'Actual Results': None,
#         'Notes': None,
#         # 'Attachment':
#     }
#     if bug.id:
#         bug_dict['id'] = bug.id
#     if bug.summary:
#         bug_dict['Summary'] = bug.summary
#     if bug.description.prerequisites:
#         bug_dict['Preconditions'] = bug.description.prerequisites.text
#     if bug.description.steps_to_reproduce:
#         steps = list()
#         for index, step in enumerate(bug.description.steps_to_reproduce):
#             # step_dict = {
#             #     "step_id": index,
#             #     "step_text": step.text
#             # }
#
#             steps.append(get_step_dict((step.cluster_index,
#                                         step.text,
#                                         GraphUtil.INDEX_CLUSTER_EXPECTED_ACTUAL_RESULT_DICT[step.cluster_index])))
#             # steps.append(step.text)
#         bug_dict['Steps to Reproduce'] = steps
#     if bug.description.expected_results:
#         bug_dict['Expected Results'] = bug.description.expected_results.text
#     if bug.description.actual_results:
#         bug_dict['Actual Results'] = bug.description.actual_results.text
#     return bug_dict


@app.route("/", methods=['GET', 'POST'])
def search():
    search_result = {
        'bugReport': None,
        'relevantBugReports': None,
        'exploratoryTestResults': None,

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
            input_bug_dict = GraphUtil.get_bug_dict(input_bug)
            search_result['bugReport'] = input_bug_dict
            # print(search_result)
            bug_list, bug_ranking_details_dict = GraphUtil.find_relevant_ranked_bugs_by_bug_id(bugs, int(search_input))
            relevant_bug_dict_list = list()
            for bug in bug_list:
                relevant_bug_dict_list.append(GraphUtil.get_relevant_bug_dict(bug, bug_ranking_details_dict[bug]))
            # only return top-50, otherwise too slow to transfer and display
            search_result['relevantBugReports'] = relevant_bug_dict_list[0:50]
            # # default: open No.1 relevant bug report and get its exploratoryTestResults
            # if search_result['relevantBugReports']:
            #     search_result['exploratoryTestResults'] = GraphUtil.get_test_reports_from_two_bugs(GraphUtil.BUG_ID_BUG_DICT[int(input_bug.id)],
            #                                                              GraphUtil.BUG_ID_BUG_DICT[int(relevant_bug_dict_list[0]['id'])])
            # print("return result")

            return jsonify(search_result)

    elif 'relevantBugId' in post_data.keys():
        bug_id = post_data['bugId']
        relevant_bug_id = post_data['relevantBugId']
        print(f"{bug_id} {relevant_bug_id}")
        test_report_dict_list = GraphUtil.get_test_reports_from_two_bugs(GraphUtil.BUG_ID_BUG_DICT[int(bug_id)],
                                                                         GraphUtil.BUG_ID_BUG_DICT[int(relevant_bug_id)])
        search_result['exploratoryTestResults'] = test_report_dict_list
        # print(f"{search_result['exploratoryTestResults']}")
        return jsonify(search_result)
    return jsonify("")


if __name__ == "__main__":
    logging.warning("Loading bugs...")
    bugs = FileUtil.load_pickle(Path(DATA_DIR, "bugs_with_step_object.json"))
    # bugs = FileUtil.load_pickle(Path(DATA_DIR, "firefox_about_logins_bugs_with_step_object.json"))
    # bugs = FileUtil.load_pickle(Path(DATA_DIR, "firefox_Preferences_bugs_with_step_object.json"))
    # bugs = FileUtil.load_pickle(Path(DATA_DIR, "Toolkit_Printing_bugs_with_step_object.json"))
    # get GraphUtil.BUG_ID_BUG_DICT key: bug_id, value: bug (Bug)
    GraphUtil.get_bug_id_bug_dict(bugs)
    # get GraphUtil.INDEX_CLUSTER_DICT key: index, value: cluster (step)
    GraphUtil.get_index_cluster_dict(bugs)
    # get GraphUtil.INDEX_CLUSTER_EXPECTED_ACTUAL_RESULT_DICT key: index,
    # value: [(bug_id, step_id, expected result, actual result)]
    GraphUtil.get_index_cluster_expected_actual_result_dict()
    # GraphUtil.get_steps(bugs)
    #
    # test_report_list = GraphUtil.get_test_reports_from_two_bugs(GraphUtil.BUG_ID_BUG_DICT[1678633], GraphUtil.BUG_ID_BUG_DICT[1577195])
    # for test_report in test_report_list:
    #     print(test_report)
    logging.warning("Start the web server...")
    app.run(host='0.0.0.0')
