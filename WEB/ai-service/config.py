import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Translate ID → EN
id_en_model_name = "Helsinki-NLP/opus-mt-id-en"
id_en_tokenizer = AutoTokenizer.from_pretrained(id_en_model_name)
id_en_model = AutoModelForSeq2SeqLM.from_pretrained(id_en_model_name).to(device)

# Summarizer
summ_model_name = "google/flan-t5-base"
summ_tokenizer = AutoTokenizer.from_pretrained(summ_model_name)
summ_model = AutoModelForSeq2SeqLM.from_pretrained(summ_model_name).to(device)

# Translate EN → ID
en_id_model_name = "Helsinki-NLP/opus-mt-en-id"
en_id_tokenizer = AutoTokenizer.from_pretrained(en_id_model_name)
en_id_model = AutoModelForSeq2SeqLM.from_pretrained(en_id_model_name).to(device)

EMOSI_SCORE_CHANGE = {
    "sangat senang": +3,
    "senang": +2,
    "cukup senang": +1,
    "netral": 0,
    "cukup sedih": -2,
    "sedih": -3,
    "sangat sedih": -5,
    "tidak diketahui": 0
}

emosi_mapping = {
    1: "sangat senang",
    2: "senang",
    3: "cukup senang",
    4: "netral",
    5: "cukup sedih",
    6: "sedih",
    7: "sangat sedih"
}