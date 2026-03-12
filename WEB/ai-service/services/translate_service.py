from config import device
import config

def translate(text, tokenizer, model):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512).to(device)
    outputs = model.generate(**inputs, max_length=512)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def translate_id_to_en(text):
    return translate(text, config.id_en_tokenizer, config.id_en_model)

def translate_en_to_id(text):
    return translate(text, config.en_id_tokenizer, config.en_id_model)