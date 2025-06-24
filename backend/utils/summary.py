import openparse
import faiss
import numpy as np
import pickle
from openai import AsyncOpenAI
from dotenv import load_dotenv


async def summarize_chunk(text, idx=None):

    load_dotenv()

    # Create the client with API key
    client = AsyncOpenAI()

    prompt = f"""Summarize the following section of a legal contract in 2-3 bullet points. Focus on obligations, durations, risks, or key terms.

{text}
"""
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a legal assistant helping summarize contracts.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error summarizing chunk {idx}: {e}")
        return None


async def summarize_whole(path):
    load_dotenv()

    # Create the client with API key
    client = AsyncOpenAI()

    basic_doc_path = path
    parser = openparse.DocumentParser()
    parsed_basic_doc = parser.parse(basic_doc_path)

    all_summaries = []

    for idx, node in enumerate(parsed_basic_doc.nodes):
        summary = summarize_chunk(node.text, idx)
        if summary:
            all_summaries.append(f"Node {idx} Summary:\n{summary}")

    final_summary = "\n\n".join(all_summaries)

    # Optional: Further condense the full summary
    final_prompt = f"""Combine and refine the following contract summaries into a concise executive summary (max 8 bullet points):

    {final_summary}
    """

    refined = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a legal assistant helping summarize contracts.",
            },
            {"role": "user", "content": final_prompt},
        ],
        temperature=0.3,
    )

    return refined.choices[0].message.content.strip()
