import logging

from tqdm import tqdm

from bug_finding.types.bug import Bugs, Bug
from bug_finding.utils.file_util import FileUtil
from bug_finding.utils.nlp_util import NLPUtil
from bug_finding.utils.path_util import PathUtil

if __name__ == "__main__":
    """
    从原始数据集中  
                 1. 保留status = "CLOSED, RESOLVED, VERIFIED"
                 2. if bug.description and bug.description.steps_to_reproduce and expected_result and actual_result
                 3. filter bugs by steps: a. remove step's serial number
                                          b. remove step which only has non_alphanumeric
                                          c. remove bug that has steps with more than STEP_MAX_TOKEN_NUM tokens
                                          d. remove bug that has more than MAX_STEP_NUM steps 
                 4. filter bugs by creation time
    """

    bugs = FileUtil.load_json(PathUtil.get_bugs_filepath("bugs"))

    bug_list = []
    logging.warning(f"filter {len(bugs)} bugs by status, description "
                    f"(steps_to_reproduce, expected_results, actual_results)")
    for bug in tqdm(bugs, ascii=True):
        # add Notes section in description.from_text(bug.description.text)
        bug = Bug.from_dict(bug)

        # if bug.product_component_pair in pc_dataset:
        if bug.status == 'CLOSED' or bug.status == 'RESOLVED' or bug.status == 'VERIFIED':
            # if bug.description and "steps to reproduce" in bug.description.text.lower():
            if bug.description and bug.description.steps_to_reproduce \
                    and bug.description.expected_results and bug.description.actual_results:
                bug_list.append(bug)
    filtered_bugs = Bugs(bug_list)
    NLPUtil.load_spacy_model()
    logging.warning(f"{filtered_bugs.get_length()} bugs left and split steps_to_reproduce section into steps")
    filtered_bugs.split_steps_to_reproduce_into_steps()
    logging.warning(f"filter {filtered_bugs.get_length()} bugs by steps")
    filtered_bugs = filtered_bugs.filter_bugs_by_step()
    logging.warning(f"has {filtered_bugs.get_length()} bugs left")
    logging.warning(f"filter bugs by creation time: 2010-04-02T16:30:02Z")
    old_bugs, recent_bugs = filtered_bugs.split_dataset_by_creation_time("2010-04-02T16:30:02Z")
    filtered_bugs = recent_bugs
    filtered_bugs.overall_bugs()
    filtered_bugs_filepath = PathUtil.get_filtered_bugs_filepath()
    FileUtil.dump_pickle(filtered_bugs_filepath, filtered_bugs)
