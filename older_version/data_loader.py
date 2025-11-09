import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss


def load_data():
    df = pd.read_csv('data/professors.csv')
    df["text"] = df.apply(lambda x: f"{x['Name']} works on {x['Research_Areas']}. {x['Summary']}", axis=1)
    return df

def build_index(df):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(df["text"].tolist(), convert_to_numpy=True)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return model,index, embeddings