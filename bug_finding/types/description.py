import logging
import re

from bug_finding.event_extraction.placeholder import Placeholder
from bug_finding.event_extraction.seed_extractor import SeedExtractor
from bug_finding.utils.nlp_util import NLPUtil, SentUtil
from bug_finding.utils.timeout_util import break_after
from config import ELEMENT_MERGE_THRESHOLD, ACTION_MERGE_THRESHOLD, STEP_MAX_TOKEN_NUM, MAX_STEP_NUM


class Section:
    """
       section includes attributes: text, concepts
       (preconditions, expected results, actual results, notes use this object)
    """

    def __init__(self, text, concepts=None):
        self.text = text
        self.concepts = concepts  # concept object 传引用

    def __repr__(self):
        return f'{self.text} - \n{self.concepts}'

    def __str__(self):
        return f'{self.text} - \n{self.concepts}'

    def __eq__(self, other):
        return self.text == other.text \
            # and self.id == other.id

    def __hash__(self):
        # print(hash(str(self)))
        return hash(str(self))

    @classmethod
    def from_section(cls, text, concepts):
        """
        Construct Section object, among them, text (string), concepts (Concept object list)
        1. remove non_alphanumeric information at the begin and end of the text
        2. extract concepts in text
        @param text: the original text
        @type text: string
        @param concepts: concept list
        @type concepts: Concept object list
        @return: section
        @rtype: Section
        """
        # remove non_alphanumeric information at the begin and end of the text
        lines = text.splitlines()  # split section text into lines
        processed_text = ""
        for line in lines:
            if not NLPUtil.is_non_alpha(line):
                # print(step)
                # line = NLPUtil.remove_serial_number(line)
                # line = SeedExtractor.replace_seed_by_placeholder(line)
                # line = NLPUtil.remove_text_between_parenthesis(line)
                processed_text = processed_text + "\n" + line
        processed_text = processed_text.strip()
        # extract concepts in processed_text
        processed_text = SeedExtractor.replace_seed_by_placeholder(processed_text)
        concepts_in_processed_text = re.findall(rf"{Placeholder.CONCEPT}\d+", processed_text, flags=0)
        processed_text = SeedExtractor.replace_placeholder_by_seed(processed_text)[0]
        if concepts_in_processed_text:
            for index, concept in enumerate(concepts_in_processed_text):
                concepts_in_processed_text[index] = SeedExtractor.replace_placeholder_by_seed(concept)[0]
                concepts_in_processed_text[index] = concepts.find_concept_by_name(concepts_in_processed_text[index])
        # have repetitive concepts
        # concepts_in_processed_text = list(set(concepts_in_processed_text))

        return cls(processed_text, concepts_in_processed_text)


class Step:
    """
    step includes attributes: step, concept, action, target, condition
                              previous_step, next_step
    """

    def __init__(self, id, bug, text, concepts=None, concepts_in_target=None, action_object=None, action=None,
                 target=None,
                 condition=None, prev_step=None, next_step=None):
        self.id = id
        self.bug = bug
        self.text = text
        self.concepts = concepts  # concept object 传引用
        self.concepts_in_target = concepts_in_target
        self.action_object = action_object
        self.action = action
        self.target = target
        self.condition = condition

        self.prev_step = prev_step  # step object
        self.next_step = next_step

        self.cluster_index = None

        # self.merge_steps_with_cossim = set()

        # self.potential_prev_steps = None
        # self.potential_next_steps = None

    def __repr__(self):
        return f'{self.id}\n https://bugzilla.mozilla.org/show_bug.cgi?id={self.bug.id}\n ' \
               f'{self.text} - (\n{self.concepts}, \n{self.concepts_in_target}, \n{self.action_object}, ' \
               f'\n{self.action}, {self.target}, {self.condition}, \n{self.cluster_index}) \n************\n'

    def __str__(self):
        return f'{self.id}\n https://bugzilla.mozilla.org/show_bug.cgi?id={self.bug.id}\n ' \
               f'{self.text} - (\n{self.concepts}, \n{self.concepts_in_target}, \n{self.action_object}, ' \
               f'\n{self.action}, {self.target}, {self.condition}, \n{self.cluster_index}) \n************\n'

    def __eq__(self, other):
        return self.text == other.text \
            # and self.id == other.id

    def __hash__(self):
        # print(hash(str(self)))
        return hash(str(self))

    @classmethod
    def from_step(cls, id, bug, step, concepts, prev_step):
        """
        Construct Step object, among them, concepts (object list), action (object), target (string), condition (string)
        also add action to category
        @param bug:
        @type bug:
        @param concepts:
        @type concepts:
        @param prev_step:
        @type prev_step:
        @param step:
        @type step:
        @return:
        @rtype:
        """
        action, target, condition, concepts_in_step, concepts_in_target = Step.extract_action_target_condition_concept_tuple(
            step)

        concept_list = set()  # concept (object) list
        concept_in_target_list = set()  # concept (object) list

        for concept_name in concepts_in_step:
            concept = concepts.find_concept_by_name(concept_name)
            if concept:
                concept_list.add(concept)
                if concept_name in concepts_in_target:
                    concept_in_target_list.add(concept)

        action_object = None

        # # concept_in_target = None
        # if target:
        #     # need to change
        #     target_embedding = NLPUtil.SBERT_MODEL.encode([target])
        #     # concept_embedding = NLPUtil.SENTENCE_TRANSFORMER(concepts.concept_name_list)
        #     pairs_list = NLPUtil.get_pairs_with_cossim_by_decreasing(target_embedding,
        #                                                              concepts.concept_name_embedding_list)
        #     top_1_pairs = NLPUtil.get_top_1_pairs_with_cossim(pairs_list)
        #     if top_1_pairs[0]['score'] >= ELEMENT_MERGE_THRESHOLD:
        #         concept_index = top_1_pairs[0]['index'][1]
        #         concept_in_target = concepts.find_concept_by_name(concepts.concept_name_list[concept_index])
        #         concept_list.add(concept_in_target)
        #         concept_in_target_list.add(concept_in_target)
        #
        # action_object = None
        # if concept_in_target_list:
        #     action_embedding = NLPUtil.SBERT_MODEL.encode([action])
        #     top_score = 0
        #     for concept in concept_in_target_list:
        #         for category_action in concept.category.actions:
        #             # concept_embedding = NLPUtil.SENTENCE_TRANSFORMER(concepts.concept_name_list)
        #             pairs_list = NLPUtil.get_pairs_with_cossim_by_decreasing(action_embedding,
        #                                                                      category_action.equivalent_embedding)
        #             top_1_pairs = NLPUtil.get_top_1_pairs_with_cossim(pairs_list)
        #             if top_1_pairs[0]['score'] > top_score:
        #                 top_score = top_1_pairs[0]['score']
        #                 action_object = category_action
        #     if top_score < ACTION_MERGE_THRESHOLD:
        #         action_object = None

        return cls(id, bug, step, concept_list, concept_in_target_list, action_object, action, target, condition,
                   prev_step)

    def is_in_the_same_path(self, step):
        """
        self and step is in the same path or not
        from self forward search
        from self back search
        @param step: the step need to be compared with self_step
        @type step: Step
        @return: true or false
        @rtype: boolean
        """
        if step is None:
            return False
        prev_step = self
        while prev_step is not None:
            if prev_step == step:
                return True
            else:
                prev_step = prev_step.prev_step
        next_step = self.next_step
        while next_step is not None:
            if next_step == step:
                return True
            else:
                next_step = next_step.next_step
        return False

    # @classmethod
    # def extract_action_target_condition_tuple(cls, step):
    #     action = None
    #     target = None
    #     condition = None
    #
    #     return

    @staticmethod
    def extract_action_target_condition_concept_tuple(text):
        """
        Have session store enabled.  -> verb + nsubj or nsubjpass
        Click the CONCEPT_13 button. -> verb + obj
        Go to CONCEPT_2              -> verb + prep + pobj
        Scroll down the CONCEPT_33.  -> verb + prt + obj
        Scroll down to CONCEPT_29.   -> verb + prt + prep + pobj
        Focus back to the CONCEPT_2 page. -> verb + advmod + prep + pobj
        I right clicked the Password field -> advmod + verb + dobj
        Right-click on the password -> advmod + punct + verb + prep + pobj
        Right click on the website address link. -> intj + verb + prep + pobj
        Observe what button is focused on.
        Try to see a password, by clicking the "eye", or copy it by clicking "copy".
        Move the mouse away, hover over it again;
        Middle click on the CONCEPT_23 and CONCEPT_22 buttons.
        *************************************************
        for obj:
        Click on one of the saved logins that has a very long username.
        Click, on, one, []
        Select any of the saved logins.
        Select, None, any, []
        In CONCEPT_6 set identity.fxaccounts.enabled = false.
        set, None, false, []
        Observe the “Go to <webite_name>” link.
        Observe, None, Go, []
        Look at the "Created/Last modified/Last used" area
        Look, at, modified, []
        Open the Beta 70.0b3 Italian build with the profile from prerequisites.
        Open, None, Italian, []
        Select CONCEPT_13
        Login to sync & logins data;
        click logins and passwords
        Delete by clicking the Remove button.
        visit URL_4
        @param doc:
        @type doc:
        @param text:
        @type text:
        @return:
        @rtype:
        """
        NLPUtil.SPACY_NLP.enable_pipe("merge_noun_chunks")
        # SpacyModel.NLP.disable_pipes("benepar")
        # logging.warning(SpacyModel.NLP.pipe_names)
        # print(SentUtil.NLP.pipe_names)
        # if not doc:
        text = SeedExtractor.replace_seed_by_placeholder(text)
        doc = NLPUtil.SPACY_NLP(text)
        # extract root verb
        root = [token for token in doc if token.head == token]  # verb
        adv_left = None  # adv to modify verb advmod 状语
        adv_right = None  # adv to modify verb advmod 状语
        prt = None  # phrasal verb particle 短语动词助词
        prep = None  # prep
        obj = None  # obj
        concepts_in_object = []
        verb_phrase = None
        # concepts = None  # concepts  need to be adjusted
        # conditions = list()  # condition
        if root:
            root = root[0]
            # extract adverbial modifier
            adv = [child for child in root.children if child.dep_ == "intj" or child.dep_ == "advmod"]
            if adv:
                adv = adv[0]
                if adv.i == root.i - 1:
                    adv_left = adv
                elif adv.i == root.i + 1:
                    adv_right = adv
            # extract dobj
            obj = [child for child in root.children if
                   child.dep_ == "dobj" or child.dep_ == "nsubjpass" or child.dep_ == "nsubj"]
            if not obj:
                # extract verb [prep]
                prep = [child for child in root.children if child.dep_ == "prep"]
                # get the object of the action (root)
                if prep:
                    # extract prep [obj]
                    prep = prep[0]
                    obj = [child for child in prep.children if child.dep_ == "pobj"]

            # extract phrasal verb particle
            prt = [child for child in root.children if child.dep_ == "prt"]
            if prt:
                prt = prt[0]
            else:
                prt = None
            # print(verb_comp)
            if adv_right and not obj and not prep:
                prep = [child for child in adv_right.children if child.dep_ == "prep"]
                # get the object of the action (root)
                if prep:
                    # extract prep [obj]
                    prep = prep[0]
                    obj = [child for child in prep.children if child.dep_ == "pobj"]
            # concepts = None
            if obj:
                obj = obj[0]
                # extract concepts from obj only
                concepts_in_object = re.findall(rf"{Placeholder.CONCEPT}\d+", str(obj), flags=0)
            else:
                obj = None
        else:
            root = None
        # concepts = re.findall(rf"{Placeholder.Concept}\d+", str(text), flags=0)
        # print(obj)
        # print(concepts)
        main_part = ""

        if root:
            # print(root.i)
            main_part = str(root)
            verb_phrase = str(root.lemma_)
        if adv_left:
            # print(adv.i)
            # adv_left = str(adv_left)
            main_part = str(adv_left) + " " + main_part
            verb_phrase = str(adv_left.lemma_) + " " + verb_phrase
        if adv_right:
            # print(adv.i)
            main_part = main_part + " " + str(adv_right)
            verb_phrase = verb_phrase + " " + str(adv_right.lemma_)
        if prt:
            # print(prt.i)
            # prt = str(prt)
            main_part = main_part + " " + str(prt)
            verb_phrase = verb_phrase + " " + str(prt.lemma_)
        if prep:
            # print(prep.i)
            # prep = str(prep)
            main_part = main_part + " " + str(prep)
            verb_phrase = verb_phrase + " " + str(prep.lemma_)
        if obj:
            # print(obj.i)
            obj = str(obj)
            obj = SeedExtractor.replace_placeholder_by_seed(obj)[0]
            main_part = main_part + " " + obj
        concepts = re.findall(rf"{Placeholder.CONCEPT}\d+", text, flags=0)
        if concepts:
            for index, concept in enumerate(concepts):
                concepts[index] = SeedExtractor.replace_placeholder_by_seed(concept)[0]
        if concepts_in_object:
            for index, concept in enumerate(concepts_in_object):
                concepts_in_object[index] = SeedExtractor.replace_placeholder_by_seed(concept)[0]

        text = SeedExtractor.replace_placeholder_by_seed(text)[0]
        conditions = Step.extract_condition(text, main_part)
        # condition = Step.extract_condition(text, verb_phrase, obj)

        return verb_phrase, obj, conditions, concepts, concepts_in_object

    @classmethod
    def extract_condition(cls, text, main_part):
        # SpacyModel.NLP.disable_pipes("benepar")
        # logging.warning(SpacyModel.NLP.pipe_names)
        conditions = list()
        # print(main_part)
        # use click to replace Verb_phrase, use button replace obj for pps extraction
        text = text.replace(main_part, "click button")
        text = SeedExtractor.replace_seed_by_placeholder(text)

        doc = NLPUtil.SPACY_NLP(text)
        prep_phrases = SentUtil.extract_prep_phrases(doc)
        for pp in prep_phrases:
            pp = SeedExtractor.replace_placeholder_by_seed(str(pp))[0]
            conditions.append(pp)

        if not conditions:
            conditions = None
        return conditions

    # @classmethod
    # def extract_condition(cls, text, main_part):
    #     print(main_part)
    #     condition = text.replace(main_part, "")
    #     # is_condition = re.sub('[^A-Za-z0-9]+', ' ', condition).strip()  # remove non-alpha-number and 首尾空格回车等
    #     # remove non-alphanumeric characters at the beginning or end of a string
    #     condition = re.sub(r"^\W+|\W+$", "", condition)
    #     if not condition:
    #         condition = None
    #     return condition


class Description:
    PREREQUISITES = {"Prerequisites", "Preconditions"}
    STEPS_TO_REPRODUCE = {"Steps to reproduce", "Steps To reproduce", "Steps To Reproduce", "Steps to Reproduce",
                          "Steps to reproduce it"}
    EXPECTED_RESULTS = {"Expected result", "Expected Result", "Expected results", "Expected Results",
                        "Expected outcome", "Expected Outcome", "Expected behavior", "Expected Behavior", "Expected"}
    ACTUAL_RESULTS = {"Actual result", "Actual Result", "Actual results", "Actual Results", "Actual outcome",
                      "Actual Outcome", "Actual behavior", "Actual Behavior", "Actual"}
    NOTES = {"Notes", "Additional notes", "Additional Notes"}
    OTHERS = {"Affected versions", "Affected Versions", "Affected platforms", "Affected Platforms",
              # "Notes", "Additional notes", "Additional Notes",
              "Regression", "Regression range", "Regression Range", "Regression window", "Regression Window",
              "Environment"}
    # \W equals to [^a-zA-Z0-9_]
    KEYWORDS = '[^a-zA-Z0-9]*\n|'.join(
        PREREQUISITES | STEPS_TO_REPRODUCE | EXPECTED_RESULTS | ACTUAL_RESULTS | NOTES | OTHERS) + '[^a-zA-Z0-9]*\n'

    PATTERNS_SECTIONS = [
        re.compile(r"(?P<TITLE>%s)(?P<SECTION>.*?)(?=%s|$)" % (KEYWORDS, KEYWORDS), re.DOTALL),
        # re.compile(r"(?P<TITLE>%s)(?P<SECTION>.*?)(?=%s|$)" % (KEYWORDS, KEYWORDS), re.DOTALL | re.I),
        # re.DOTALL - Make the '.' special character match any character at all, including a newline;
        #           - without this flag, '.' will match anything except a newline.
        # re.I - ignore Upper or lower case
    ]

    def __init__(self,
                 text=None,
                 prerequisites=None,
                 steps_to_reproduce=None,
                 expected_results=None,
                 actual_results=None,
                 notes=None):
        self.text = text
        self.prerequisites = prerequisites
        self.steps_to_reproduce = steps_to_reproduce
        self.expected_results = expected_results
        self.actual_results = actual_results
        self.notes = notes

    def __repr__(self):
        return f'{self.text}'

    def __str__(self):
        return f'{self.text}'

    @classmethod
    def from_text(cls, text):
        """
        split text into four + one sections
        prerequisites, steps_to_reproduce, expected_result, actual_result, notes
        @param text: bug description
        @type text: string
        @return: Description
        @rtype: object
        """
        prerequisites, steps_to_reproduce, expected_result, actual_result, notes = cls.extract_sections(text)
        # ************************************************
        if steps_to_reproduce:
            # steps_to_reproduce = steps_to_reproduce.splitlines()  # split section text into lines
            #
            # # split step into sents
            # new_sents = list()
            # # logging.warning("split step into sents...")
            # for step in steps_to_reproduce:
            #     sents = NLPUtil.sentence_tokenize_by_spacy(step)
            #     # sents = NLPUtil.sentence_tokenize_by_nltk(step)
            #     for sent in sents:
            #         sent = NLPUtil.remove_serial_number(sent)
            #         if not NLPUtil.is_non_alphanumeric(sent):
            #             if len(sent.split()) > STEP_MAX_TOKEN_NUM:  # if step has too much tokens,
            #                 # then steps to reproduce maybe consist of one paraphrase
            #                 # print(step)
            #                 return cls(text, prerequisites, None, expected_result, actual_result, notes)
            #             new_sents.append(sent)
            # if len(new_sents) > MAX_STEP_NUM:
            #     return cls(text, prerequisites, None, expected_result, actual_result, notes)
            # steps_to_reproduce = new_sents

            # processed_steps = list()
            # for step in steps_to_reproduce:
            #     # if not NLPUtil.is_non_alphanumeric(step):
            #     step = NLPUtil.remove_serial_number(step)
            #     if not NLPUtil.is_non_alphanumeric(step):
            #         # when the number of tokens in sentence > 512,
            #         # spacy benepar: ValueError: Sentence of length 960 (in sub-word tokens)
            #         # exceeds the maximum supported length of 512
            #         # "Sky is blue." token from spacy: token_num: 4; len(step.split()): 3
            #         if len(step.split()) > STEP_MAX_TOKEN_NUM:  # if step has too much tokens,
            #                                                     # then steps to reproduce maybe consist of one paraphrase
            #             # print(step)
            #             return cls(text, prerequisites, None, expected_result, actual_result, notes)
            #         processed_steps.append(step)
            # steps_to_reproduce = processed_steps

        # steps_to_reproduce = cls.extract_detail(steps_to_reproduce)
        # ************************************************
        # for index, atomic_step in enumerate(atomic_steps):
        #     atomic_steps[index] = SeedExtractor.replace_placeholder_by_seed(atomic_step)
            return cls(text, prerequisites, steps_to_reproduce, expected_result, actual_result, notes)

        return cls(text, prerequisites, None, expected_result, actual_result, notes)

    @classmethod
    def extract_sections(cls, text):
        prerequisites = None
        steps_to_reproduce = None
        expected_result = None
        actual_result = None
        notes = None
        for pattern in Description.PATTERNS_SECTIONS:
            # print(pattern)
            matching_rs = pattern.finditer(text)  # matching result
            for rs in matching_rs:
                section_title = rs.groupdict()["TITLE"]
                section_title = re.sub('[^A-Za-z0-9]+', ' ',
                                       section_title).strip()  # remove non-alpha-number and 首尾空格回车等
                # print(section_title)
                section_text = rs.groupdict()["SECTION"]
                # ************************************************
                # section_text = cls.extract_steps(section_text)
                # ************************************************
                # print(section_text)
                # classify section into four classifications
                if section_title in Description.PREREQUISITES:
                    prerequisites = section_text
                elif section_title in Description.STEPS_TO_REPRODUCE:
                    steps_to_reproduce = section_text
                elif section_title in Description.EXPECTED_RESULTS:
                    expected_result = section_text
                elif section_title in Description.ACTUAL_RESULTS:
                    actual_result = section_text
                elif section_title in Description.NOTES:
                    notes = section_text

        return prerequisites, steps_to_reproduce, expected_result, actual_result, notes

    @classmethod
    def extract_detail(cls, steps_to_reproduce):
        """
        extract detail from steps to reproduce
        """
        steps = []
        # step_texts = convert section to step texts
        prev_step = None
        for step in steps_to_reproduce:

            action_target_condition_tuple = SentUtil.extract_action_target_condition(step)
            # print(step)
            # print(action_object_condition_tuple)
            step, element = SeedExtractor.replace_placeholder_by_seed(step)
            target = None
            conditions = list()
            action = action_target_condition_tuple[0]
            # if action_target_condition_tuple[0]:
            #     action = SeedExtractor.replace_placeholder_by_seed(str(action_target_condition_tuple[0]))
            if action_target_condition_tuple[1]:
                target = SeedExtractor.replace_placeholder_by_seed(str(action_target_condition_tuple[1]))[0]
            if action_target_condition_tuple[2]:
                for condition in action_target_condition_tuple[2]:
                    conditions.append(SeedExtractor.replace_placeholder_by_seed(str(condition))[0])

            step = Step(step, element, action, target, conditions)
            step.prev_step = prev_step
            if prev_step is not None:
                prev_step.next_step = step
            prev_step = step
            steps.append(step)
        return steps

    @classmethod
    def extract_steps(cls, section):
        """
        # 1. split section into steps
        # 2. remove non alphanumeric steps
        # 3. remove serial number from the step begining
        # 4. replace seed by placeholder
        5. split sentences into atomic steps
        """
        # steps = section.splitlines()  # split section text into lines
        # logging.warning("SpaCy NLP for Constituency Dependency...")

        processed_steps = []
        for step in section:
            # if not NLPUtil.is_non_alphanumeric(step):
            #     # print(step)
            #     step = NLPUtil.remove_serial_number(step)

            # step = SeedExtractor.replace_seed_by_placeholder(step)
            # step = NLPUtil.remove_text_between_parenthesis(step)
            atomic_steps = [step]
            # if step has cconj
            if SentUtil.SENT_HAS_CCONJ_LIST[SentUtil.SENT_LIST.index(step)]:
                # step_doc = SentUtil.SENT_CONS_DOC_LIST[SentUtil.SENT_LIST.index(step)]
                # have unlimited recursion
                try:
                    # atomic_steps = cls.split_step_into_atomic_steps(step)
                    # atomic_steps = SentUtil.split_atomic_sents_by_benepar(step, list(step_doc.sents))
                    atomic_steps = SentUtil.split_atomic_sents_by_benepar(step)

                    # if atomic_steps is None:
                    #     logging.warning(f'{step}: runtime exceeded')
                    #     atomic_steps = [step]
                except RuntimeError:
                    logging.warning(f'{step}: maximum recursion depth exceeded')
            # else:
            #     atomic_steps = [step]
            # # extract action, object, condition tuple
            # SentUtil.extract_action_object_condition_tuple()

            for index, atomic_step in enumerate(atomic_steps):
                atomic_steps[index] = SeedExtractor.replace_placeholder_by_seed(atomic_step)[0].strip()
                if atomic_steps[index] and atomic_steps[index][-1].isalnum():
                    atomic_steps[index] = atomic_steps[index] + '.'
            # print(atomic_steps)
            # input()
            processed_steps.extend(atomic_steps)
            #
            # processed_steps.append(step)

        return processed_steps

    @classmethod
    # @break_after(2)  # 等待2s,还未运行结束，return None
    def split_step_into_atomic_steps(cls, step):
        # print(step)
        # atomic_steps = list()
        atomic_steps = SentUtil.split_atomic_sents_by_benepar(step)
        # for step in steps:
        #     steps = SentUtil.split_atomic_sents_by_comma(step)
        #     atomic_steps.extend(steps)
        # print(atomic_steps)

        return atomic_steps
