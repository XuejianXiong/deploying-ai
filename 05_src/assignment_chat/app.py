import os
from utils.logger import get_logger
from dotenv import load_dotenv

from langchain_core.messages import HumanMessage, AIMessage
import gradio as gr

from main import get_exercise_chat_agent

_logs = get_logger(__name__)

load_dotenv('../.secrets')
if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError("Missing OPENAI_API_KEY environment variable")


#######################################
# Run the Model
#######################################
agent=get_exercise_chat_agent()
 
def exercise_chat(message: str, history: list[dict]) -> str:
    langchain_messages = []
    n = 0
    print(f"History: {history}")
    for msg in history:
        if msg['role'] == 'user':
            langchain_messages.append(HumanMessage(content=msg['content']))
        elif msg['role'] == 'assistant':
            langchain_messages.append(AIMessage(content=msg['content']))
            n += 1
    langchain_messages.append(HumanMessage(content=message))

    state = {
        "messages": langchain_messages,
        "llm_calls": n
    }

    response = agent.invoke(
                    state, 
                    config={
                        "tags": ["production", "senior-user"],
                        "metadata": {"session_id": "test-session-001"}
                }
)
    return response['messages'][len(response['messages']) - 1].content


#######################################
# Open the UI
#######################################
chat = gr.ChatInterface(
    fn=exercise_chat,
    type="messages"
)

if __name__ == "__main__":
    _logs.info('Starting Exercise Chat App...')
    chat.launch()
