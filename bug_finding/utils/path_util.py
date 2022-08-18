from pathlib import Path

from config import DATA_DIR, OUTPUT_DIR


class PathUtil:

    @staticmethod
    def get_bugs_filepath(filename):
        return Path(DATA_DIR, f"{filename}.json")

    @staticmethod
    def get_filtered_bugs_filepath():
        return Path(DATA_DIR, "filtered_bugs.json")

    @staticmethod
    def get_filtered_bugs_with_atomic_steps_filepath():
        return Path(DATA_DIR, "filtered_bugs_with_atomic_steps.json")

    @staticmethod
    def get_filtered_bugs_with_atomic_steps_object_filepath():
        return Path(DATA_DIR, "filtered_bugs_with_atomic_object_steps.json")

    @staticmethod
    def get_categories_filepath():
        return Path(DATA_DIR, "categories.json")

    @staticmethod
    def get_concepts_filepath():
        return Path(DATA_DIR, "concepts.json")

    @staticmethod
    def get_actions_filepath():
        return Path(DATA_DIR, "actions.json")

    # @staticmethod
    # def get_filtered_bugs_with_stp_filepath():
    #     return Path(DATA_DIR, "filtered_bugs_with_stp.json")
    #
    # @staticmethod
    # def get_filtered_bugs_without_stp_filepath():
    #     return Path(DATA_DIR, "filtered_bugs_without_stp.json")

    @staticmethod
    def get_pc_filepath():
        return Path(DATA_DIR, "product_component.json")
    #
    # @staticmethod
    # def get_events_filepath():
    #     return Path(OUTPUT_DIR, "events.csv")
    #

    @staticmethod
    def get_specified_product_component_bug_filepath(product_component_pair):
        return Path(DATA_DIR, f"{product_component_pair.product}_{product_component_pair.component}_bug.csv")

    # @staticmethod
    # def get_specified_product_component_bug_with_stp_filepath(product_component_pair):
    #     return Path(OUTPUT_DIR, f"{product_component_pair.product}_{product_component_pair.component}_bug_with_stp.csv")
    #
    # @staticmethod
    # def get_specified_product_component_bug_without_stp_filepath(product_component_pair):
    #     return Path(OUTPUT_DIR, f"{product_component_pair.product}_{product_component_pair.component}_bug_without_stp.csv")

    @staticmethod
    def get_search_result_filepath(search_input):
        return Path(OUTPUT_DIR, "search_result", f"{search_input}.xlsx")
