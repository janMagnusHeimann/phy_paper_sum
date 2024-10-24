from datasets import Dataset
from transformers import (
    AutoTokenizer, AutoModelForSequenceClassification,
    Trainer, TrainingArguments
)

import pandas as pd

# Load the dataset from the CSV file
data = pd.read_csv('processed_papers.csv')

# Convert the dataframe into a Hugging Face Dataset object
dataset = Dataset.from_pandas(data)

# Load the SciBERT tokenizer
tokenizer = AutoTokenizer.from_pretrained("allenai/scibert_scivocab_uncased")


# Tokenize the dataset
def tokenize_function(examples):
    return tokenizer(
        examples["full_text"], padding="max_length", truncation=True)


tokenized_dataset = dataset.map(tokenize_function, batched=True)


# Load the pre-trained SciBERT model for sequence classification
model = AutoModelForSequenceClassification.from_pretrained(
    "allenai/scibert_scivocab_uncased", num_labels=2)

# Define the training arguments
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
)

# Define the trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
)

# Fine-tune the model
trainer.train()

# Save the fine-tuned model
model.save_pretrained('./fine_tuned_scibert')
tokenizer.save_pretrained('./fine_tuned_scibert')

print("Model fine-tuned and saved at './fine_tuned_scibert'")
