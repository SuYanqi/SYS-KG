import os
from pathlib import Path

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root Directory

DATA_DIR = str(Path(ROOT_DIR, "data"))

OUTPUT_DIR = str(Path(ROOT_DIR, "output"))

SEED_FILTER_COUNT_THRESHOLD = 2  # SeedExtractor.filter_seeds_by_count(seed_count_dict)

ELEMENT_MERGE_THRESHOLD = 0.85

ACTION_MERGE_THRESHOLD = 0.85

STEP_MERGE_THRESHOLD = 0.85

SPACY_BATCH_SIZE = 1024

SBERT_BATCH_SIZE = 64

STEP_MAX_TOKEN_NUM = 64

MAX_STEP_NUM = 20

