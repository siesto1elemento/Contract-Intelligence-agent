import os
import pickle
import faiss
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
from openparse import processing, DocumentParser


def rag_embedding(path: str):

    load_dotenv()
    client = OpenAI()

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
        # print(f"Node {idx}------------------------")
        # print(node.text)
        nodes_text.append(node.text)

    response = client.embeddings.create(
        input=nodes_text, model="text-embedding-3-small"
    )

    embeddings = [item.embedding for item in response.data]

    with open("embeddings.pkl", "wb") as f:
        pickle.dump(nodes_text, f)

    dimension = len(embeddings[0])
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype("float32"))
    faiss.write_index(index, "index.faiss")


#     query = "what is the leave policy"
#     query_response = client.embeddings.create(
#     input=query,
#     model="text-embedding-3-small"
# )


#     query_embedding = query_response.data[0].embedding
#     D, I = index.search(np.array([query_embedding]).astype('float32'), k=3)

#     for idx in I[0]:
#         print(f"{idx}-----------------------")
#         node = nodes_text[idx]
#         print(node)
