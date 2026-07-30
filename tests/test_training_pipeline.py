"""Tests for Phase 2 Foundation Model Training Pipeline."""

import pytest
from zkai.training.corpus_loader import CorpusLoader
from zkai.training.corpus_cleaner import CorpusCleaner
from zkai.training.deduplicator import Deduplicator
from zkai.training.streaming_corpus import StreamingCorpus
from zkai.training.token_packing import TokenPacker
from zkai.training.curriculum import CurriculumLearning
from zkai.training.recipe import TrainingRecipe
from zkai.training.instruction_tuning import InstructionTuner
from zkai.training.sft import SFTTrainer
from zkai.training.preference import PreferenceOptimizer, RewardModel
from zkai.neural.module import Module


def test_corpus_cleaner():
    cleaner = CorpusCleaner(strip_html=True, remove_extra_whitespace=True, min_length=5)
    raw = "<p>Hello   world!  This is   a test.</p>"
    cleaned = cleaner.clean_text(raw)
    assert cleaned == "Hello world! This is a test."


def test_deduplicator():
    dedup = Deduplicator(similarity_threshold=0.8)
    docs = ["The quick brown fox jumps", "The quick brown fox jumps", "Something completely different"]
    exact = dedup.deduplicate_exact(docs)
    assert len(exact) == 2


def test_token_packer():
    packer = TokenPacker(max_seq_len=10)
    seqs = [[1, 2, 3], [4, 5, 6, 7]]
    packed = packer.pack_sequences(seqs)
    assert len(packed) >= 1
    assert packed[0]["input_ids"].shape[1] == 10


def test_curriculum_learning():
    curriculum = CurriculumLearning()
    data = ["short text", "a much longer sentence with many more words inside it", "med text here"]
    sorted_data = curriculum.sort_by_difficulty(data)
    assert len(sorted_data[0].split()) <= len(sorted_data[-1].split())


def test_training_recipe():
    recipe = TrainingRecipe(name="gpt_recipe", epochs=5, learning_rate=1e-4)
    r_dict = recipe.to_dict()
    assert r_dict["epochs"] == 5
    rec2 = TrainingRecipe.from_dict(r_dict)
    assert rec2.name == "gpt_recipe"


def test_instruction_tuner():
    tuner = InstructionTuner(template_type="alpaca")
    formatted = tuner.format_sample(instruction="Solve math", output="42")
    assert "Solve math" in formatted
    assert "42" in formatted
