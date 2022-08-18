import logging
import re

from tqdm import tqdm

from bug_finding.event_extraction.placeholder import Placeholder
from bug_finding.utils.nlp_util import NLPUtil
from bug_finding.utils.timeout_util import break_after
from config import SEED_FILTER_COUNT_THRESHOLD

logging.basicConfig(format='%(asctime)s %(message)s')


class SeedExtractor:
    """
    extract seeds:
      if seed is url:
        replace by URL_n
            1. rule-based (regex)
      elif seed is element:
        replace by ELEMENT_n
            1. 1-gram <- rule-based (regex)
            2. n-gram <- n-gram (5 >= n >= 2)
    """
    PATTERN_SEEDS = [
        # generalization?! -> title or sentence case convention + filter method(frequency)
        # re.compile(r"\S+:\S+", re.DOTALL),
        # re.compile(r"about:\S+[a-zA-Z]", re.DOTALL),
        re.compile(r"about:[a-zA-Z#?=.-]+[a-zA-Z]", re.DOTALL),  # about:*
        re.compile(r"[A-Z][A-Za-z]+ & [A-Z][A-Za-z]+", re.DOTALL),  # * & *  # title case convention
        re.compile(r'"(.*?)"', re.DOTALL),  # "*"
        re.compile(r'“(.*?)”', re.DOTALL),  # “*”
        re.compile(r'\'(.*?)\'', re.DOTALL),  # '*'
        re.compile(r'\[(.*?)\]', re.DOTALL),  # [*]

        # re.compile(r'(?:\'|\"|“)(.*?)(?:\'|\"|”)', re.DOTALL)  # "*" “*” '*'
        # re.compile(r"(?<!\A)(?<!\.)\s+[A-Z]\w+", re.DOTALL),
    ]

    KEYWORDS_FOR_SENTENCE_CASE = '|'.join(["button", "dialog", "section", "page", "tab", "key", "option", "text",
                                           "link", "hyperlink", "panel", "dropdown", "menu", "checkbox", "radio",
                                           "menu", "field"])

    PLACEHOLDER_SEED_DICT = dict()  # key: placeholder, value: seed
    PLH_DICT_KEYS_BY_PLH_LEN = None
    PLH_DICT_KEYS_BY_SEED_LEN = None

    @staticmethod
    def extract_seeds_by_title_sentence_case_convention(text, seed_count_dict):
        """
        1. Use Title case convention to extract seeds
        2. if seeds only contain >1 words, then add into seed_list
           else: turn into Sentence case convention
                           (Start from seed and
                           all lowercase words spaces and
                           End by SeedExtractor.KEYWORDS_FOR_SENTENCE_CASE)
        @param seed_count_dict:
        @type seed_count_dict:
        @param text:
        @type text:
        @return:
        @rtype:
        """
        # remove punctuations at the end of the text
        idx = next((i for i, j in enumerate(reversed(text)) if j.isalnum()), 0)
        text = text[:-idx]
        # print(text)

        match_list = list()
        pre_word = ""
        words_in_text = text.split()
        for index, word in enumerate(words_in_text):
            if index != 0:
                if re.fullmatch(r"[A-Z][a-z]*", word):
                    pre_word = pre_word + " " + word

                elif pre_word.strip():

                    match_list.append(pre_word.strip())
                    pre_word = ""
        if pre_word:
            match_list.append(pre_word)

        # print(match_list)
        # seeds = list()
        for match in match_list:
            if len(match.split()) > 1:
                seed = match.strip()
                seed_count_dict[seed] = seed_count_dict.get(seed, 0) + 1
                # seeds.append(match.strip())
            else:
                result = re.search(f'{match}([a-z ]+)({SeedExtractor.KEYWORDS_FOR_SENTENCE_CASE})', text)
                # print(result)
                if result:
                    if result.group(1).strip():
                        match = match + result.group(1)
                    # seeds.append(match.strip())
                    seed = match.strip()
                    seed_count_dict[seed] = seed_count_dict.get(seed, 0) + 1

        return seed_count_dict

    # @classmethod
    # def extract_seeds_urls_from_bugs(cls, bugs):
    #     """
    #     extract seeds and urls from steps to reproduce in descriptions of bugs
    #     @param bugs:
    #     @type bugs: Bugs
    #     @return: SeedExtractor.PLACEHOLDER_DICT (key = placeholder, value = seed or url)
    #     @rtype: dict
    #     """
    #     text = ""
    #     for bug in tqdm(bugs, ascii=True):
    #         # text = text + "\n" + bug.description.text
    #         if bug.description.steps_to_reproduce:
    #             # for step in bug.description.steps_to_reproduce:
    #             text = text + "\n" + bug.description.steps_to_reproduce
    #
    #     # print(len(text))
    #
    #     # extract urls and seeds and get placeholder
    #     logging.warning("Extract URLs...")
    #     urls = SeedExtractor.extract_urls(text)
    #     logging.warning("URLs Extraction Done")
    #
    #     logging.warning("Extract Seeds...")
    #     seeds = SeedExtractor.extract_seeds(text)
    #     logging.warning("Seeds Extraction Done")
    #     logging.warning("Get placeholder dict...")
    #     SeedExtractor.get_placeholder_dict(seeds, urls)
    #     logging.warning("Placeholder Dict Done")

    @staticmethod
    def extract_urls_from_bugs(bugs):
        urls = set()
        for bug in tqdm(bugs, ascii=True):
            # print(bug.id)
            text = bug.summary
            if bug.description.prerequisites:
                text = text + " " + bug.description.prerequisites
            if bug.description.steps_to_reproduce:
                for step in bug.description.steps_to_reproduce:
                    text = text + " " + step
                # text = text + " " + bug.description.steps_to_reproduce
            if bug.description.expected_results:
                text = text + " " + bug.description.expected_results
            if bug.description.actual_results:
                text = text + " " + bug.description.actual_results
            if bug.description.notes:
                text = text + " " + bug.description.notes
            # text = text.strip()
            if text:
                text_urls = SeedExtractor.extract_urls_by_regex(text)
                if text_urls:
                    urls = urls.union(text_urls)

            # if bug.description.steps_to_reproduce:
            #     text = bug.description.steps_to_reproduce
            #     # text = bug.description.text
            #     urls = urls.union(SeedExtractor.extract_urls_by_regex(text))
        return urls

    @staticmethod
    def extract_seeds_from_bugs(bugs):
        seed_count_dict = dict()
        for bug in tqdm(bugs, ascii=True):
            text = bug.summary
            if bug.description.prerequisites:
                text = text + " " + bug.description.prerequisites
            if bug.description.steps_to_reproduce:
                for step in bug.description.steps_to_reproduce:
                    text = text + " " + step
                # text = text + " " + bug.description.steps_to_reproduce
            if bug.description.expected_results:
                text = text + " " + bug.description.expected_results
            if bug.description.actual_results:
                text = text + " " + bug.description.actual_results
            if bug.description.notes:
                text = text + " " + bug.description.notes
            if text:
                seed_count_dict = SeedExtractor.extract_seeds_by_regex(text, seed_count_dict)

            # if bug.description.steps_to_reproduce:
            #     # for step in bug.description.steps_to_reproduce:
            #     text = bug.description.steps_to_reproduce
            #     # text = bug.description.text
            #     seed_count_dict = SeedExtractor.extract_seeds_by_regex(text, seed_count_dict)

        seed_count_dict = SeedExtractor.filter_seeds_by_count(seed_count_dict)

        seeds = seed_count_dict.keys()
        return seeds

    @staticmethod
    def extract_seeds_from_external_knowledge():
        """
        extract seeds from external knowledge
        external knowledge: Placeholder.EXTERNAL_KNOWLEDGE_DICT
        @return: seeds
        @rtype: set()
        """
        seeds = set()
        for category in Placeholder.EXTERNAL_KNOWLEDGE_DICT.keys():
            concept_related_dict = Placeholder.EXTERNAL_KNOWLEDGE_DICT[category]
            seeds = seeds | concept_related_dict.keys()
        return seeds

    @staticmethod
    def replace_seed_by_placeholder(text):
        # sorting dictionary by length of values (seeds) from long to short,
        # if not, create new login will be replaced by new login
        # if not placeholders:
        if not SeedExtractor.PLH_DICT_KEYS_BY_SEED_LEN:
            SeedExtractor.PLH_DICT_KEYS_BY_SEED_LEN = sorted(SeedExtractor.PLACEHOLDER_SEED_DICT,
                                                             key=lambda k: len(SeedExtractor.PLACEHOLDER_SEED_DICT[k]),
                                                             reverse=True)

        for seed_placeholder in SeedExtractor.PLH_DICT_KEYS_BY_SEED_LEN:
            seed_value = SeedExtractor.PLACEHOLDER_SEED_DICT[seed_placeholder]

            if seed_value in text:
                # print(seed_value)
                # text = text.replace(seed_value, seed_placeholder)
                # print(text)
                # print(seed_placeholder)

                # text = re.sub(rf'(?:\'|\"|“)*{seed_value}(?:\'|\"|“)*', seed_placeholder, text)
                original_text = text
                text = text.replace(seed_value, seed_placeholder)
                text = re.sub(rf'(?:\'|\"|“|\[)*{seed_placeholder}(?:\'|\"|“|”|\])*', seed_placeholder, text)
                # find add 'the' before placeholder will increase the dependency parser effectiveness ##################
                # maybe not

                # text = re.sub(rf'(?:\'|\"|“|\[)*{seed_placeholder}(?:\'|\"|“|”|\])*', f'the {seed_placeholder}', text)
                # Edit the password -> Edit is not the button "Edit", just a verb,
                # so there is a space '\s' before {seed_placeholder}
                # if not re.findall(rf"\s{seed_placeholder}([^0-9a-zA-Z]+|$)", text, flags=0):
                all_seed_placeholder = re.findall(rf"{seed_placeholder}", text, flags=0)
                # print(all_seed_placeholder)
                specific_seed_placeholder = re.findall(rf"(\s{seed_placeholder}[^0-9a-zA-Z]+|\s{seed_placeholder}$)",
                                                       text, flags=0)
                # print(specific_seed_placeholder)
                if len(all_seed_placeholder) != len(specific_seed_placeholder):
                    text = original_text

        return text

    @staticmethod
    def replace_placeholder_by_seed(text):
        # Sort dictionary by key (placeholder) length
        element = list()
        if not SeedExtractor.PLH_DICT_KEYS_BY_PLH_LEN:
            SeedExtractor.PLH_DICT_KEYS_BY_PLH_LEN = sorted(SeedExtractor.PLACEHOLDER_SEED_DICT, key=len, reverse=True)
        # if not sorted by reverse, then element-16 placed by element-1
        # for seed_placeholder, seed_value in sorted(SeedExtractor.PLACEHOLDER_DICT.items(), reverse=True):
        for seed_placeholder in SeedExtractor.PLH_DICT_KEYS_BY_PLH_LEN:
            seed_value = SeedExtractor.PLACEHOLDER_SEED_DICT[seed_placeholder]
            if seed_placeholder in text:
                text = text.replace(seed_placeholder, seed_value)
                # find add 'the' before placeholder will increase the dependency parser effectiveness ##################
                # maybe not
                # text = text.replace(f'the {seed_placeholder}', seed_value)

                element.append(seed_value)
                # text = re.sub(rf'(?:\'|\"|“)*{seed_value}(?:\'|\"|“)*', seed_placeholder, text)
        return text, element

    @staticmethod
    def get_placeholder_dict(seeds, urls):
        # placeholder_dict = dict()
        for index, seed in tqdm(enumerate(seeds)):
            seed_placeholder = f"{Placeholder.CONCEPT}{index + 1}"
            SeedExtractor.PLACEHOLDER_SEED_DICT[seed_placeholder] = SeedExtractor.PLACEHOLDER_SEED_DICT.get(
                seed_placeholder,
                seed)

        for index, url in tqdm(enumerate(urls)):
            url_placeholder = f"{Placeholder.URL}{index + 1}"
            SeedExtractor.PLACEHOLDER_SEED_DICT[url_placeholder] = SeedExtractor.PLACEHOLDER_SEED_DICT.get(
                url_placeholder, url)

        SeedExtractor.PLH_DICT_KEYS_BY_SEED_LEN = sorted(SeedExtractor.PLACEHOLDER_SEED_DICT,
                                                         key=lambda k: len(SeedExtractor.PLACEHOLDER_SEED_DICT[k]),
                                                         reverse=True)
        SeedExtractor.PLH_DICT_KEYS_BY_PLH_LEN = sorted(SeedExtractor.PLACEHOLDER_SEED_DICT, key=len, reverse=True)

        return SeedExtractor.PLACEHOLDER_SEED_DICT

    # @staticmethod
    # def extract_seeds(text):
    #     seed_count_dict = dict()
    #     seed_count_dict = SeedExtractor.extract_seeds_by_regex(text, seed_count_dict)
    #     seed_count_dict = SeedExtractor.filter_seeds_by_count(seed_count_dict)
    #     seeds = seed_count_dict.keys()
    #     return seeds

    @staticmethod
    def extract_seeds_by_regex(text, seed_count_dict):
        for pattern in SeedExtractor.PATTERN_SEEDS:
            # print(pattern)
            # text = "i am about:logins "
            matching_rs = pattern.findall(text)  # matching result
            # print(matching_rs)
            for rs in matching_rs:
                rs = rs.strip()  # remove space at the begining and the end
                # ********** need to design further *********
                # if rs:
                # remove rs = null and remove all lower-case, space phrases
                if len(rs) > 1 and not re.search(r'^[a-z\s]*$', rs):
                    seed_count_dict[rs] = seed_count_dict.get(rs, 0) + 1
        return seed_count_dict

    @staticmethod
    def extract_seeds_by_n_gram(text, n_threshold, seed_count_dict):
        pass

    @staticmethod
    def filter_seeds_by_count(seed_count_dict):
        filtered_seed_count_dict = dict(seed_count_dict)  # The dict() constructor makes a shallow copy
        for seed in seed_count_dict.keys():
            if seed_count_dict[seed] < SEED_FILTER_COUNT_THRESHOLD:
                filtered_seed_count_dict.pop(seed)
        return filtered_seed_count_dict

    @staticmethod
    @break_after(1)  # matching_rs = pattern.findall(text)  等待1s,还未运行结束，return None
    def extract_urls_by_regex(text):
        urls = set()
        for pattern in NLPUtil.PATTERN_URL:
            # print("#################################################################")
            # print(text)

            matching_rs = pattern.findall(text)  # matching result
            # print(matching_rs)
            for rs in matching_rs:
                # rs = rs.strip()  # remove space at the begining and the end
                if rs:  # remove rs = null
                    urls.add(rs[0])
        return urls
