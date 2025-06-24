from fastapi import WebSocket
from fastapi import APIRouter
from utils import retrieve_chunks
from openai import AsyncOpenAI

client = AsyncOpenAI()


router = APIRouter()

@router.websocket("/ws")
async def chat_stream(websocket: WebSocket):
    await websocket.accept()
    while True:
        query = await websocket.receive_text()
        chunks = await retrieve_chunks(query)
        context = "\n\n".join(chunks)

        system_prompt = (
            "You are an AI assistant. You must only answer questions based on the provided context.\n"
            "If the answer is not in the context, say: **'I'm sorry, I don't have enough information to answer that.'**\n"
            "Format your answer in Markdown. Use bullet points or numbered lists if applicable.\n"
            "Be concise, accurate, and don't include information not present in the context.\n\n"
            f"Context:\n{context}"
        )

        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            temperature=0.3,
        )

        answer = response.choices[0].message.content
        await websocket.send_text(answer)









