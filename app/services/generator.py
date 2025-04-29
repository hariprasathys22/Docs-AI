import lmstudio as lms
from fastapi.concurrency import run_in_threadpool
from app.config import LM_MODEL_NAME, LMSTUDIO_HOST, LMSTUDIO_PORT

server_addr = f"{LMSTUDIO_HOST}:{LMSTUDIO_PORT}"
client = lms.Client(api_host=server_addr)

chat_model = client.llm.model(LM_MODEL_NAME)

async def call_deepseek(question: str, chunks: list[str]) -> str: 
    """
    Sends the user question plus retrieved chunks as context to DeepSeek,
    returns the assistant’s completion text.
    """
    system_prompt = (
        "You are an assistant that relies solely on the provided context. "
        "Do not search anywhere else. If no relevant context is provided, "
        "respond with 'No relevant information available'. Analyze the context "
        "and make a sentence and reply for the given question alone. "
        "Do not use any other information."
    )
    chat_payload: dict = {
        "messages": [
            {"role": "system", "content": system_prompt},
            *[
                {"role": "user", "content": f"[source:{i}]\n{txt}"}
                for i, txt in enumerate(chunks, start=1)
            ],
            {"role": "user", "content": question},
        ]
    }
    response = await run_in_threadpool(
        chat_model.respond,
        chat_payload,
    )
    return response.content