import os
import time
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()
SQL_PLANNER_ID = os.getenv("AZURE_SQL_PLANNER_ASSISTANT_ID")

def ask_sql_planner(question: str, client: AzureOpenAI, thread_id: str) -> tuple[str, list]:
    """
    Use the SQL Planner Assistant to generate T-SQL from user's question,
    using a given thread ID for context preservation.
    Assumes the assistant's behavior is configured via system instructions in Azure.
    """
 
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=question
    )

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=SQL_PLANNER_ID
    )

    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        if run_status.status in ["completed", "failed", "cancelled"]:
            break
        time.sleep(1)

    messages = client.beta.threads.messages.list(thread_id=thread_id)
    reply = messages.data[0].content[0].text.value.strip()

    steps = client.beta.threads.runs.steps.list(thread_id=thread_id, run_id=run.id)
    log = [vars(s) for s in steps.data] if steps.data else []

    return reply, log