from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import ask_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    thread_id: str | None = None 

@app.post("/chat")
async def chat(req: ChatRequest):
    result = ask_agent(req.message, req.thread_id) 
    return {
        "reply": result["reply"],
        "thinking_log": result["thinking_log"],
        "thread_id": result["thread_id"]
    }