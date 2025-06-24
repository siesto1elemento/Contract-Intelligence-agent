import pickle
import faiss
import numpy as np
from openai import AsyncOpenAI


async def embed(text):
    client = AsyncOpenAI()
    response = await client.embeddings.create(
        input=[text], model="text-embedding-3-small"
    )
    return response.data[0].embedding


async def retrieve_chunks(query: str) -> list[str]:

    with open("embeddings.pkl", "rb") as f:
        nodes_text = pickle.load(f)

    index = faiss.read_index("index.faiss")

    query_text = query
    query_embedding = await embed(query_text)
    query_vector = np.array([query_embedding], dtype="float32")

    k = 5
    distance, indices = index.search(query_vector, k)

    chunks = []

    for idx in indices[0]:
        if 0 <= idx < len(nodes_text):
            chunks.append(nodes_text[idx])

    return chunks
