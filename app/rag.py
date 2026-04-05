import os
import numpy as np
import faiss
from openai import OpenAI

client = OpenAI()

documents = []
index = None

def load_documents():
    docs = []
    folder = "data/rules"

    for file in os.listdir(folder):
        if file.endswith(".xml"):
            with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
                docs.append(f.read())

    return docs

def chunk_text(text, size=500):
    return [text[i:i+size] for i in range(0, len(text), size)]

def get_embedding(text):
    return client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    ).data[0].embedding

def build_index():
    global documents, index

    raw_docs = load_documents()

    documents = []
    for doc in raw_docs:
        documents.extend(chunk_text(doc))

    vectors = [get_embedding(doc) for doc in documents]

    dim = len(vectors[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(vectors).astype("float32"))

    print("Index built:", len(documents))

def retrieve(query, k=3):
    q_vec = get_embedding(query)
    D, I = index.search(np.array([q_vec]).astype("float32"), k)

    return [documents[i] for i in I[0]]
