# summarizer.py
import os
import time
from typing import List, Dict
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()
SUMMARIZER_ASSISTANT_ID = os.getenv("AZURE_SUMMARIZER_ASSISTANT_ID")

def ask_summarizer(question: str, data: List[Dict] | str, client: AzureOpenAI, thread_id: str) -> tuple[str, list]:
    # Prepare input message content
    if isinstance(data, str):
        context = data
    elif isinstance(data, list) and data:
        context = f"{data[:30]}"
    else:
        context = "No data was returned."

    content = f"User question: {question}\n\nContext:\n{context}"

    # Send user message
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=content
    )

    # Run assistant
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=SUMMARIZER_ASSISTANT_ID
    )

    # Poll
    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        if run_status.status in ["completed", "failed", "cancelled"]:
            break
        time.sleep(1)

    # Get response
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    reply = messages.data[0].content[0].text.value.strip()

    steps = client.beta.threads.runs.steps.list(thread_id=thread_id, run_id=run.id)
    log = [vars(s) for s in steps.data] if steps.data else []

    return reply, log