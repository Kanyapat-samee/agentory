import os
import time
import json
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()
INTENT_CLASSIFIER_ID = os.getenv("AZURE_INTENT_CLASSIFIER_ASSISTANT_ID")

def classify_intent(message: str, client: AzureOpenAI, thread_id: str) -> tuple[dict, list]:

    #Add user message
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message
    )

    #Run assistant
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=INTENT_CLASSIFIER_ID
    )

    #Poll until complete
    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        if run_status.status in ["completed", "failed", "cancelled"]:
            break
        time.sleep(1)

    #Extract and parse response
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    raw = messages.data[0].content[0].text.value.strip()

    try:
        parsed = json.loads(raw)
        intent = parsed.get("intent", "unknown")
        response = parsed.get("response", None)
    except json.JSONDecodeError:
        # fallback (legacy format)
        intent = "unknown"
        response = None

    #Thinking log
    steps = client.beta.threads.runs.steps.list(thread_id=thread_id, run_id=run.id)
    log = [vars(s) for s in steps.data] if steps.data else []

    return {"intent": intent, "response": response}, log