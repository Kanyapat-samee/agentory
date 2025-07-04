import os
import time
from dotenv import load_dotenv
from openai import AzureOpenAI
from typing import Optional

#Import Sub-Agents (Tools)
from intent_classifier import classify_intent
from sql_planner import ask_sql_planner
from summarizer import ask_summarizer
from query_executor import execute_sql

#Load environment variables
load_dotenv()

#Setup Azure OpenAI Client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

#Main Agent Entry Point
def ask_agent(message: str, thread_id: Optional[str] = None) -> dict:
    thinking_log = {}

    # Step 0: Manage Thread
    if thread_id:
        thread = client.beta.threads.retrieve(thread_id)
    else:
        thread = client.beta.threads.create()
    thread_id = thread.id

    # Step 1: Intent Detection
    intent_output, intent_log = classify_intent(message, client, thread_id)
    intent = intent_output.get("intent")
    thinking_log["intent"] = intent_log

    if intent in ["general", "unknown"]:
        return {
            "reply": intent_output.get(
                "response",
                "I'm here to help with warehouse-related questions. Feel free to ask!"
            ),
            "thinking_log": thinking_log,
            "thread_id": thread_id
        }

    # Step 2: SQL Planning
    sql_query, planner_log = ask_sql_planner(message, client, thread_id)
    thinking_log["planner"] = planner_log

    if not sql_query:
        return {
            "reply": "ไม่สามารถวาง SQL ได้จากคำถามนี้ กรุณาระบุให้ชัดเจนขึ้น",
            "thinking_log": thinking_log,
            "thread_id": thread_id
        }

    # Step 3: SQL Execution
    result_rows = execute_sql(sql_query)
    thinking_log["executor"] = {
        "query": sql_query,
        "rows": result_rows[:3]
    }

    # Step 4: Summarization
    summary, sum_log = ask_summarizer(message, result_rows, client, thread_id)
    thinking_log["summarizer"] = sum_log

    return {
        "reply": summary,
        "thinking_log": thinking_log,
        "thread_id": thread_id
    }