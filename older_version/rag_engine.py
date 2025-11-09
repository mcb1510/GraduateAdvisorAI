import numpy as np
from transformers import pipeline

# Use text2text-generation for FLAN models
generator = pipeline("text2text-generation", model="google/flan-t5-base")

def retrieve_info(query, model, index, df, k=2):
    q_emb = model.encode([query], convert_to_numpy=True)
    D, I = index.search(np.array(q_emb), k)
    results = df.iloc[I[0]]
    context = "\n".join(results["text"].tolist())
    return context

def generate_response(query, context):
    prompt = (
        f"You are an academic advisor AI. Use only the context below.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}\nAnswer:"
    )
    output = generator(prompt, max_length=200, num_return_sequences=1)
    return output[0]["generated_text"].split("Answer:")[-1].strip()
