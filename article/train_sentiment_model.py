import pandas as pd
import nltk
from sklearn.model_selection import train_test_split
from datasets import Dataset
from transformers import RobertaTokenizer, RobertaForSequenceClassification, Trainer, TrainingArguments
import torch
import joblib
from sklearn.metrics import accuracy_score, classification_report
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download necessary NLTK data
nltk.download('stopwords')
nltk.download('wordnet')

# Load your original dataset and new dataset
df = pd.read_csv("sentimentdataset.csv")

# Detect encoding of the new dataset
import chardet
with open('train.csv', 'rb') as f:
    result = chardet.detect(f.read())
    print(result)

# Use the detected encoding for reading the new dataset
df_new = pd.read_csv("train.csv", encoding=result['encoding'])

# Display columns in both datasets
print(f"Columns in original dataset: {df.columns}")
print(f"Columns in new dataset: {df_new.columns}")

# Filter relevant columns from both datasets
df_filtered = df[['Text', 'Sentiment']]  # Original dataset columns
df_new_filtered = df_new[['text', 'sentiment']]  # New dataset columns, adjusted for casing

# Rename columns to make them consistent for both datasets
df_new_filtered.columns = ['Text', 'Sentiment']  # Renaming to match the original dataset

# Combine the two datasets
df_combined = pd.concat([df_filtered, df_new_filtered], ignore_index=True)

# Class distribution check after combining datasets
class_counts = df_combined['Sentiment'].value_counts()
print("Class distribution in the target variable:")
print(class_counts)

# Remove classes with only one sample
classes_to_remove = class_counts[class_counts == 1].index
df_combined = df_combined[~df_combined['Sentiment'].isin(classes_to_remove)]

# Confirm class distribution after removing rare classes
class_counts = df_combined['Sentiment'].value_counts()
print("Class distribution after removing rare classes:")
print(class_counts)

# Check for invalid sentiment labels
valid_sentiments = ['negative', 'positive', 'neutral']
invalid_sentiments = df_combined[~df_combined['Sentiment'].isin(valid_sentiments)]
if not invalid_sentiments.empty:
    print(f"Invalid sentiment labels found:\n{invalid_sentiments}")
    # Optionally, drop or fix the invalid rows
    df_combined = df_combined[df_combined['Sentiment'].isin(valid_sentiments)]

# Text Preprocessing
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    if isinstance(text, str):
        text = text.translate(str.maketrans("", "", string.punctuation)).lower()
        tokens = text.split()
        tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
        return " ".join(tokens)
    else:
        return ""

# Apply preprocessing to the 'Text' column from the combined dataset
df_combined['Text'] = df_combined['Text'].apply(preprocess_text)

# Convert to Hugging Face Dataset
dataset = Dataset.from_pandas(df_combined[['Text', 'Sentiment']])

# Map sentiments to integer labels (0: negative, 1: positive, 2: neutral)
label_map = {'negative': 0, 'positive': 1, 'neutral': 2}
dataset = dataset.map(lambda x: {'label': label_map[x['Sentiment']]})

# Check for any rows with invalid labels
invalid_labels = dataset.filter(lambda x: x['label'] == -1)
if len(invalid_labels) > 0:
    print(f"Invalid labels found: {invalid_labels}")
    # Remove rows with invalid labels
    dataset = dataset.filter(lambda x: x['label'] != -1)

# Split dataset into train and test
train_dataset, test_dataset = dataset.train_test_split(test_size=0.3).values()

# Load a pre-trained tokenizer from Hugging Face
tokenizer = RobertaTokenizer.from_pretrained('roberta-base')

def tokenize_function(examples):
    return tokenizer(examples['Text'], padding='max_length', truncation=True)

# Tokenize the dataset
train_dataset = train_dataset.map(tokenize_function, batched=True)
test_dataset = test_dataset.map(tokenize_function, batched=True)

# Load the pre-trained model
model = RobertaForSequenceClassification.from_pretrained('roberta-base', num_labels=3)

# Training arguments
training_args = TrainingArguments(
    output_dir='./results',
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
)

# Define the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    tokenizer=tokenizer,
    compute_metrics=lambda p: {
        'accuracy': accuracy_score(p.predictions.argmax(axis=1), p.label_ids),
        'classification_report': classification_report(p.label_ids, p.predictions.argmax(axis=1), output_dict=True)
    },
)

# Train the model
trainer.train()

# Evaluate the model
results = trainer.evaluate()

# Save the trained model
model.save_pretrained('./sentiment_model_huggingface')
tokenizer.save_pretrained('./sentiment_model_huggingface')

# Save results for later use
joblib.dump(results, 'model_results.pkl')

# To predict sentiment for new input text
def analyze_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    outputs = model(**inputs)
    prediction = torch.argmax(outputs.logits, dim=-1).item()
    return prediction

# Example usage of the analyze_sentiment function
new_text = "I love this product! It's amazing."
predicted_sentiment = analyze_sentiment(new_text)
print(f"The predicted sentiment for the text is: {['negative', 'positive', 'neutral'][predicted_sentiment]}")
