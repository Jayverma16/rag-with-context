# Quickest way to get started
from datasets import load_dataset

# SQuAD 2.0
ds = load_dataset("rajpurkar/squad_v2")

# Natural Questions
ds = load_dataset("google-research-datasets/natural_questions")

# RAGAS built-in sample
from ragas.testset import TestsetGenerator  # auto-generates RAG eval data from your docs