from config import summ_tokenizer, summ_model, device

def summarize_text_en(text_en):
    prompt = f"""
    Summarize the text below while keeping the main details.

    Text:
    {text_en}
    """

    inputs = summ_tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True).to(device)

    summary_ids = summ_model.generate(
        **inputs,
        max_length=110,
        min_length=30,
        num_beams=4,
        length_penalty=1.3,
        no_repeat_ngram_size=4,
        early_stopping=True
    )

    return summ_tokenizer.decode(summary_ids[0], skip_special_tokens=True).strip()