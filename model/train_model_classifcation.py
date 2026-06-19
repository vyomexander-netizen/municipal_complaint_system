import pandas as pd

from datasets import Dataset
from sklearn.model_selection import train_test_split
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    DataCollatorWithPadding,
    TrainingArguments,
    Trainer
)

MODEL_NAME = "distilbert/distilbert-base-uncased"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

df = pd.read_csv("complaints.csv")

train_data, temp_data = train_test_split(
    df,
    test_size=0.30,
    random_state=42,
    shuffle=True,
    stratify=df["category"]
)

validation_data, test_data = train_test_split(
    temp_data,
    test_size=0.50,
    random_state=42,
    shuffle=True,
    stratify=temp_data["category"]
)

label2id = {
    "Electricity": 0,
    "Water": 1,
    "Roads": 2,
    "Waste": 3,
    "Public Safety": 4
}

id2label = {
    0: "Electricity",
    1: "Water",
    2: "Roads",
    3: "Waste",
    4: "Public Safety"
}

def prepare_dataframe(data):
    data = data.copy()
    data["label"] = data["category"].map(label2id)
    return data[["text", "label"]]

train_dataset = Dataset.from_pandas(
    prepare_dataframe(train_data),
    preserve_index=False
)

validation_dataset = Dataset.from_pandas(
    prepare_dataframe(validation_data),
    preserve_index=False
)

test_dataset = Dataset.from_pandas(
    prepare_dataframe(test_data),
    preserve_index=False
)

def tokenize_input(data):
    return tokenizer(
        data["text"],
        truncation=True,
        max_length=128
    )

train_dataset = train_dataset.map(tokenize_input, batched=True)
validation_dataset = validation_dataset.map(tokenize_input, batched=True)
test_dataset = test_dataset.map(tokenize_input, batched=True)

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=len(label2id),
    id2label=id2label,
    label2id=label2id
)

training_args = TrainingArguments(
    output_dir="./results",
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=3,
    learning_rate=2e-5,
    save_strategy="epoch",
    eval_strategy="epoch",
    load_best_model_at_end=True
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=validation_dataset,
    data_collator=data_collator
)

trainer.train()



trainer.save_model("saved_models/department")
tokenizer.save_pretrained("saved_models/department")










