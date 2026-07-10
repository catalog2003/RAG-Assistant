import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM
)

from New.Backend.config import LLM_MODEL_NAME

device = (
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)

print("Loading Hugging Face LLM...")

tokenizer = AutoTokenizer.from_pretrained(
    LLM_MODEL_NAME,
    trust_remote_code=True
)

model = AutoModelForCausalLM.from_pretrained(
    LLM_MODEL_NAME
).to(device)

print(f"LLM loaded on {device}")

def build_prompt(
    query: str,
    contexts: list[dict]
):
    context_text = "\n\n".join([
        f"[Document: {ctx['document']} | Page {ctx['page']}]\n{ctx['text']}"
        for ctx in contexts
    ])

    return f"""
Context:

{context_text}

Question:
{query}

Answer:
"""

def ask_hf_llm(
    prompt: str,
    max_new_tokens=200
):
    messages = [
        {
            "role": "system",
            "content": """
You are a document QA assistant.

Rules:
1. Answer only from context.
2. Keep answer concise.
3. Summarize.
4. If missing say:
I cannot find that information in the document.
"""
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    chat_prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(
        chat_prompt,
        return_tensors="pt",
        truncation=True,
        max_length=3500
    ).to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            repetition_penalty=1.15,
            no_repeat_ngram_size=4
        )

    generated_tokens = outputs[0][
        inputs.input_ids.shape[1]:
    ]

    answer = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    )

    return answer.strip()