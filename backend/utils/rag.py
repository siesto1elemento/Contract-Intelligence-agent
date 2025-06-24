import os
import pickle
import faiss
import numpy as np
from openai import AsyncOpenAI
from dotenv import load_dotenv
from openparse import processing, DocumentParser


async def rag_embedding(path: str):

    load_dotenv()
    client = AsyncOpenAI()

    semantic_pipeline = processing.SemanticIngestionPipeline(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        model="text-embedding-3-small",
        min_tokens=64,
        max_tokens=1024,
    )
    parser = DocumentParser(
        processing_pipeline=semantic_pipeline,
    )
    parsed_content = parser.parse(path)

    nodes_text = []

    for idx, node in enumerate(parsed_content.nodes):
        nodes_text.append(node.text)

    response = await client.embeddings.create(
        input=nodes_text, model="text-embedding-3-small"
    )

    embeddings = [item.embedding for item in response.data]

    with open("embeddings.pkl", "wb") as f:
        pickle.dump(nodes_text, f)

    dimension = len(embeddings[0])
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype("float32"))
    faiss.write_index(index, "index.faiss")



