import torch
from torch.utils.data import DataLoader, Dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from datasets import load_dataset, Dataset as HFDataset
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import os
import re
import random
import kagglehub

# Set the device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

x = pd.read_csv("Mental_Health_FAQ.csv")
freq_question= pd.DataFrame()
freq_question["question"] = x["Questions"]
freq_question["response"] = x["Answers"]

# Load your local data
concel = pd.read_csv(".\\oneHotData.csv")

# Remove HTML tags
def remove_html_tags(text):
    return re.sub(r'<.*?>', '', text)

for column in concel.select_dtypes(include='object').columns:
    concel[column] = concel[column].apply(remove_html_tags)

# Extract questions and responses from local data
concel_train = pd.DataFrame()
concel_train['question'] = concel['questionFull']
concel_train['response'] = concel['answerText']

# Load Empathetic Dialogues dataset
empathetic_dataset = load_dataset("empathetic_dialogues")
empathetic_df = empathetic_dataset['train'].to_pandas()
empathetic_df = empathetic_df.sort_values(by=['conv_id', 'utterance_idx']).reset_index(drop=True)

# Create question-response pairs
def create_question_response_pairs(df):
    conversations = []
    current_conv_id = None
    current_qa_pairs = []

    for _, row in df.iterrows():
        conv_id = row['conv_id']
        utterance = row['utterance']
        if conv_id != current_conv_id:
            if current_qa_pairs:
                conversations.append(current_qa_pairs)
            current_qa_pairs = []
            current_conv_id = conv_id
        if len(current_qa_pairs) % 2 == 0:
            current_qa_pairs.append({'question': utterance, 'response': ''})
        else:
            current_qa_pairs[-1]['response'] = utterance
    if current_qa_pairs:
        conversations.append(current_qa_pairs)
    return conversations

# Apply question-response pairs and convert to DataFrame
conversations = create_question_response_pairs(empathetic_df)
data = [pair for conv in conversations for pair in conv if pair['response']]
empathetic_train_data = pd.DataFrame(data)

# Load Mental Health Chatbot Dataset
hf_train_data = pd.read_parquet("hf://datasets/heliosbrahma/mental_health_chatbot_dataset/data/train-00000-of-00001-01391a60ef5c00d9.parquet")
if 'text' in hf_train_data.columns:
    hf_train_data = hf_train_data.rename(columns={'text': 'combined_text'})
if 'response' not in hf_train_data.columns:
    hf_train_data['response'] = None

def split_human_assistant(text):
    human_part = re.search(r"<HUMAN>:(.*?)<ASSISTANT>:", text, re.DOTALL)
    assistant_part = re.search(r"<ASSISTANT>:(.*)", text, re.DOTALL)
    question = human_part.group(1).strip() if human_part else ''
    response = assistant_part.group(1).strip() if assistant_part else ''
    return question, response

# Split and apply to columns
hf_train_data[['question', 'response']] = hf_train_data['combined_text'].apply(
    lambda x: pd.Series(split_human_assistant(x))
)

# Load local MentalLLaMA data
train_instruction_data_path = r"MentalLLaMA/train_data/instruction_data"
train_complete_data_path = r"MentalLLaMA/train_data/complete_data"

def load_all_csv_from_directory(directory_path):
    dataframes = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                df = pd.read_csv(file_path)
                dataframes.append(df)
    return pd.concat(dataframes, ignore_index=True) if dataframes else pd.DataFrame()

train_instruction_df = load_all_csv_from_directory(train_instruction_data_path) if os.path.exists(train_instruction_data_path) else pd.DataFrame()
train_complete_df = load_all_csv_from_directory(train_complete_data_path) if os.path.exists(train_complete_data_path) else pd.DataFrame()
local_train_data = pd.concat([train_instruction_df, train_complete_df], ignore_index=True)
local_train_data = local_train_data.drop(columns=['Unnamed: 0'], errors='ignore').dropna(subset=['query', 'gpt-3.5-turbo'], how='all')
local_train_data['question'] = local_train_data['query'].fillna('') + ' ' + local_train_data['post'].fillna('')
local_train_data['response'] = local_train_data['gpt-3.5-turbo']
local_train_data = local_train_data[['question', 'response']]

# Combine datasets
train_data = pd.concat(
    [hf_train_data[['question', 'response']], local_train_data[['question', 'response']], empathetic_train_data[['question', 'response']], concel_train[['question', 'response']], freq_question[['question', 'response']]],
    ignore_index=True
).dropna(subset=['question', 'response']).reset_index(drop=True)
train_data = train_data.applymap(lambda x: x.replace("_comma_", "") if isinstance(x, str) else x)

# Define extended politeness templates
politeness_starters = [
    "I’d be delighted to help you!",
    "Please allow me to assist you in understanding!",
    "It’s my pleasure to guide you! ",
    "Thank you for reaching out. Let’s Talk!",
    "I’m here to make things easier for you! "
]
politeness_enders = [
    "I hope this information helps you on your way!",
    "If there’s anything more you need, I’m here to help.",
    "Let’s work together to find the best solution.",
    "Remember, I'm here to support you whenever you need.",
    "Please don’t hesitate to ask if you have any more questions."
]

# Apply politeness templates to responses
def add_random_politeness(row):
    # 30% chance to add polite start
    if random.random() < 0.2:
        polite_start = random.choice(politeness_starters) + " "
    else:
        polite_start = ""

    # 30% chance to add polite end
    if random.random() < 0.1:
        polite_end = " " + random.choice(politeness_enders)
    else:
        polite_end = ""

    return f"{polite_start}{row['response']}{polite_end}"

train_data['response'] = train_data.apply(add_random_politeness, axis=1)

# Prepare data for model training
def concatenate_conversations(row):
    return f"<|startoftext|>User: {row['question']}\nAssistant: {row['response']}<|endoftext|>"

train_data['text'] = train_data.apply(concatenate_conversations, axis=1)
train_texts, val_texts = train_test_split(train_data['text'], test_size=0.1, random_state=42)

# Load the tokenizer and model
# from transformers import GPT2LMHeadModel, GPT2TokenizerFast

# model_name = 'gpt2-medium'  # You can choose 'gpt2-medium', 'gpt2-large', etc., depending on your computational resources
# tokenizer = GPT2TokenizerFast.from_pretrained(model_name)
# model = GPT2LMHeadModel.from_pretrained(model_name)

from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "microsoft/DialoGPT-medium"  # Choose 'DialoGPT-small', 'DialoGPT-medium', or 'DialoGPT-large'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)


# Add special tokens to the tokenizer and model
special_tokens = {'pad_token': '<|pad|>', 'eos_token': '<|endoftext|>', 'bos_token': '<|startoftext|>'}
num_added_toks = tokenizer.add_special_tokens(special_tokens)
model.resize_token_embeddings(len(tokenizer))

# Tokenize the datasets
def tokenize_function(examples):
    return tokenizer(examples['text'], truncation=True, max_length=512, padding='max_length')

train_dataset = HFDataset.from_dict({'text': train_texts})
val_dataset = HFDataset.from_dict({'text': val_texts})

train_dataset = train_dataset.map(tokenize_function, batched=True, remove_columns=['text'])
val_dataset = val_dataset.map(tokenize_function, batched=True, remove_columns=['text'])

# Set the format for PyTorch tensors
train_dataset.set_format(type='torch', columns=['input_ids', 'attention_mask'])
val_dataset.set_format(type='torch', columns=['input_ids', 'attention_mask'])

# Define a custom collate function
def data_collator(features):
    return {
        'input_ids': torch.stack([f['input_ids'] for f in features]),
        'attention_mask': torch.stack([f['attention_mask'] for f in features]),
        'labels': torch.stack([f['input_ids'] for f in features]),
    }

# Define training arguments
training_args = TrainingArguments(
    output_dir='./results',
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=4,  # Adjust based on your GPU memory
    per_device_eval_batch_size=2,
    save_steps=1000,
    save_total_limit=2,
    logging_steps=500,
    evaluation_strategy='steps',
    eval_steps=1000,
    learning_rate=8e-5,
    weight_decay=0.005,
    fp16=torch.cuda.is_available(),
    report_to="none",  # To disable logging to WandB or other platforms
    gradient_accumulation_steps=2,
)

# Initialize the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    data_collator=data_collator,
)

# Start training
trainer.train()

# Save the trained model
trainer.save_model('./trained_polite_model')

# Save model
current_path = os.getcwd()
model_save_path = os.path.join(current_path, 'trained_polite_model')
model.save_pretrained(model_save_path)

tokenizer.save_pretrained(model_save_path)


# Function to generate responses
def generate_response(question, max_length=150):
    input_text = f"<|startoftext|>User: {question}\nAssistant:"
    input_ids = tokenizer.encode(input_text, return_tensors='pt').to(device)
    model.eval()
    with torch.no_grad():
        output = model.generate(
            input_ids,
            max_length=max_length,
            do_sample=True,
            top_p=0.95,
            top_k=60,
            temperature=0.7,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.convert_tokens_to_ids('<|endoftext|>'),
        )
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    # Extract the assistant's response
    assistant_response = response.split('Assistant:')[-1].strip()
    return assistant_response


