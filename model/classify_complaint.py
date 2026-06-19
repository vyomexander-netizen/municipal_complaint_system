import os
from transformers import pipeline

MODEL_ID = os.getenv("DEPARTMENT_MODEL_ID")

_classifier = None

def get_classifier():
    global _classifier
    if _classifier is None:
        _classifier = pipeline(
            "text-classification",
            model=MODEL_ID,
            tokenizer=MODEL_ID
        )
    return _classifier

def classify_complaint(text):
    result = get_classifier()(
        text,
        truncation=True,
        max_length=128
    )
    return result[0]["label"]