import os
import torch
from transformers import GPT2LMHeadModel, GPT2TokenizerFast

# Load the model and tokenizer
current_path = os.getcwd()
model_save_path = os.path.join(current_path, 'models/trained_polite_model')
model = GPT2LMHeadModel.from_pretrained(model_save_path)
tokenizer = GPT2TokenizerFast.from_pretrained(model_save_path)

# Move the model to the device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.eval()
model.to(device)

# Function to generate responses using GPT-2 model
recent_inputs = []

def generate_response(question, max_length=150):
    # Memorize the recent user inputs (up to 5)
    if len(recent_inputs) >= 5:
        recent_inputs.pop(0)
    recent_inputs.append(question)

    # Include recent inputs in the model's context
    context = "".join([f"User: {inp}Assistant:" for inp in recent_inputs])
    input_text = f"<|startoftext|>{context}"
    input_ids = tokenizer.encode(input_text, return_tensors='pt').to(device)
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
    assistant_response = response.split('Assistant:')[-1].strip()
    return assistant_response
