import os
from transformers import pipeline

MODEL_ID = os.getenv("DEPARTMENT_MODEL_ID")

classifier = pipeline(
    "text-classification",
    model=MODEL_ID,
    tokenizer=MODEL_ID
)

def classify_complaint(text):
    result = classifier(
        text,
        truncation=True,
        max_length=128
    )
    return result[0]["label"]
