import logging
from pathlib import Path

from bug_finding.event_extraction.seed_extractor import SeedExtractor

from bug_finding.types.entity import Category
from bug_finding.types.product_component_pair import ProductComponentPair
from bug_finding.utils.file_util import FileUtil
from bug_finding.utils.list_util import ListUtil
from bug_finding.utils.nlp_util import NLPUtil
from bug_finding.utils.path_util import PathUtil
from config import DATA_DIR
import sys

if __name__ == "__main__":
    sys.setrecursionlimit(250)  # split_atomic_steps has unlimited recursion, use this to limit the recursion

    # get dataset for extracting urls and seeds
    bugs = FileUtil.load_pickle(PathUtil.get_filtered_bugs_filepath())

    print(bugs.get_length())
    # print(bugs.overall_bugs())

    # product = "Toolkit"
    # component = "Printing"
    # bugs = bugs.get_specified_product_component_bugs(ProductComponentPair("Firefox", "Preferences"))
    # bugs = bugs.get_specified_product_component_bugs(ProductComponentPair("Firefox", "about:logins"))
    # bugs = bugs.get_specified_product_component_bugs(ProductComponentPair(product, component))

    # extract urls and seeds and get placeholder
    logging.warning("Extract URLs...")
    urls = SeedExtractor.extract_urls_from_bugs(bugs)
    logging.warning("Extract Seeds from external knowledge...")
    seeds_from_external_knowledge = SeedExtractor.extract_seeds_from_external_knowledge()
    logging.warning("Extract Seeds from bugs...")
    seeds_from_bugs = SeedExtractor.extract_seeds_from_bugs(bugs)
    # seeds = seeds_from_bugs
    logging.warning("Extract Seeds from ftl...")
    category_element_dict = FileUtil.load_json(Path(DATA_DIR, "category_element_dict.json"))
    # component = "about_preferences"
    # ftl_filename = "preferences_ftl.json"
    # html_filename = "preferences_from_scrape_url.xhtml"
    # component = "about_logins"
    # ftl_filename = "aboutLogins_ftl.json"
    # html_filename = "aboutLogins.html"
    # ftl_file_directory = Path("/Users", "suyanqi", "Desktop", "print")
    # html_file_directory = Path("/Users", "suyanqi", "Desktop", "print")
    # category_element_dict = Element.get_category_element_dict(ftl_file_directory, html_file_directory)
    # category_element_dict = Element.get_category_element_dict(Path(DATA_DIR, "firefox_gui", "about_preferences"),
    #                                                           Path(DATA_DIR, "firefox_gui", "about_preferences"))
    print(category_element_dict)
    category_element_dict['Others'] = list()
    # category_element_dict = Element.get_category_element_dict(component, ftl_filename, html_filename)
    seeds_from_ftl = set(ListUtil.convert_nested_list_to_flatten_list(category_element_dict.values()))
    seeds = seeds_from_ftl | seeds_from_bugs | seeds_from_external_knowledge
    # seeds = seeds | seeds_from_bugs
    # for category, element_list in category_element_dict.items():
    #     print(category)
    #     print(f"\t{element_list}")

    # seeds = category_element_dict.values()
    logging.warning("Get SeedExtractor.PLACEHOLDER_DICT...")
    SeedExtractor.get_placeholder_dict(seeds, urls)
    for key, value in SeedExtractor.PLACEHOLDER_SEED_DICT.items():
        print(f"{key}: {value}")

    logging.warning("replace urls and concepts by placeholder for steps")
    bugs.replace_by_placeholder()  # has a todo list

    logging.warning("Loading spacy model and sbert model...")
    NLPUtil.load_spacy_model()
    NLPUtil.load_sbert_model()
    # split sections in description into atomic_steps
    """
    Use SpacyModel.NLP enable "benepar" and "merge_noun_chunks"
    """
    logging.warning("Split steps_to_reproduce into atomic_steps...")
    # logging.warning("Split sections (preconditions, steps_to_reproduce, expected_results, actual_results, #notes) in description into atomic_steps...")
    bugs.extract_steps()

    logging.warning("Save filtered_bugs with atomic steps...")
    FileUtil.dump_pickle(PathUtil.get_filtered_bugs_with_atomic_steps_filepath(), bugs)

    NLPUtil.SPACY_NLP.disable_pipes("benepar")
    # extract categories from bugs
    """
    Use SpacyModel.NLP disable "benepar" and disable "merge_noun_chunks"
    """
    logging.warning("Extract categories for concepts from bugs...")
    category_concept_dict = bugs.extract_categories()
    print(category_concept_dict)
    # for category, element_list in category_concept_dict.items():
    #     print(category)
    #     print(f"\t{element_list}")

    # categories, concepts = Category.get_static_part(category_element_dict)
    # for category in categories:
    #     print(category)
    """
    SBertModel.SENTENCE_TRANSFORMER.encode
    """
    logging.warning("Merging concepts from External_Knowledge and elements from ftl and concepts from bugs...")
    categories, concepts, actions = Category.get_static_part(category_element_dict,
                                                             category_concept_dict)

    FileUtil.dump_pickle(PathUtil.get_categories_filepath(), categories)
    FileUtil.dump_pickle(PathUtil.get_concepts_filepath(), concepts)
    FileUtil.dump_pickle(PathUtil.get_actions_filepath(), actions)

    for category in categories:
        print(category)

    """
        SpacyModel.NLP.enable_pipe("merge_noun_chunks")
        SpacyModel.NLP.disable_pipes("benepar")
        SBertModel.SENTENCE_TRANSFORMER.encode
    """
    logging.warning("Transform sections into objects...")
    # concepts = Concepts(categories.get_concepts())
    bugs.transform_sections_into_objects(concepts, actions)
    FileUtil.dump_pickle(PathUtil.get_filtered_bugs_with_atomic_steps_object_filepath(), bugs)

    # FileUtil.dump_pickle(Path(DATA_DIR, "firefox_about_logins_bugs_with_step_object_without_merge.json"), bugs)
    #
    # bugs = FileUtil.load_pickle(Path(DATA_DIR, "firefox_about_logins_bugs_with_step_object.json"))
    """
    https://www.sbert.net/examples/applications/paraphrase-mining/README.html
    """
    """
        SBertModel.SENTENCE_TRANSFORMER.encode
    """
    logging.warning("Merging steps...")
    bugs.merge_steps_by_fast_clustering(NLPUtil.SBERT_MODEL)

    # for bug in bugs:
    #     print(f"https://bugzilla.mozilla.org/show_bug.cgi?id={bug.id}")
    #     if bug.description.steps_to_reproduce:
    #         for step in bug.description.steps_to_reproduce:
    #             print(step)
    #     print(bug.description.prerequisites)
    #     print(bug.description.expected_results)
    #     print(bug.description.actual_results)
    #     print(bug.description.notes)
    sys.setrecursionlimit(10000)  # RecursionError: maximum recursion depth exceeded while pickling an object
    # FileUtil.dump_pickle(Path(DATA_DIR, "firefox_preferences_bugs_with_step_object.json"), bugs)
    # FileUtil.dump_pickle(Path(DATA_DIR, f"firefox_about_logins_bugs_with_step_object.json"), bugs)
    # FileUtil.dump_pickle(Path(DATA_DIR, f"{product}_{component}_bugs_with_step_object.json"), bugs)
    FileUtil.dump_pickle(Path(DATA_DIR, "bugs_with_step_object.json"), bugs)


