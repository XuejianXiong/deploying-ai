import sys
import os
import operator
from typing_extensions import TypedDict, Annotated
from typing import Literal
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain_core.messages import AnyMessage
from langchain_core.messages import SystemMessage
from langchain_core.messages import ToolMessage
from langgraph.graph import StateGraph, START, END

from tools_exercise import get_body_exercise
from tools_mental import get_mental_activity
from tools_search import get_web_search
from prompts import return_instructions

load_dotenv('../.secrets')
if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError("Missing OPENAI_API_KEY environment variable")

MY_TOOLS = [get_body_exercise, get_mental_activity, get_web_search]


#######################################
# Build the LLM model with tools
#######################################
def get_model_with_tools():
    model = init_chat_model(
        "openai:gpt-4o-mini",
        temperature=0.7,
        base_url='https://k7uffyg03f.execute-api.us-east-1.amazonaws.com/prod/openai/v1', 
        api_key='any value',
        default_headers={"x-api-key": os.getenv('API_GATEWAY_KEY')}
    )

    # Augment the LLM with tools    
    model_with_tools = model.bind_tools(MY_TOOLS)
    
    return model_with_tools


#######################################
# Define State
#######################################
class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int


#######################################
# Define Model Node
#######################################
def llm_call(state: dict):
    model_with_tools = get_model_with_tools()
    call_count = state.get('llm_calls', 0)
    system_prompt = return_instructions()

    if call_count == 0:
        status_update = "\n[SYSTEM NOTE: This is the first response. You MUST include your high-energy Pob greeting before anything else.]"
    else:
        status_update = "\n[SYSTEM NOTE: Mid-session. Skip greetings.]"

    return {
        "messages": [
            model_with_tools.invoke(
                [SystemMessage(content=system_prompt + status_update)] 
                + state["messages"]
            )
        ],
        "llm_calls": call_count + 1
    }


#######################################
# Define Tool Node
#######################################
def tool_node(state: dict):
    """Performs the tool call"""
    tools_by_name = {tool.name: tool for tool in MY_TOOLS}

    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
    
    return {"messages": result}


#######################################
# Define Edge Logic
#######################################
def should_continue(state: MessagesState) -> Literal["tool_node", END]:
    """
    Decide if we should continue the loop 
    or stop based upon whether the LLM made a tool call.
    """

    messages = state["messages"]
    last_message = messages[-1]

    # If the LLM makes a tool call, then perform an action
    if last_message.tool_calls:
        return "tool_node"

    # Otherwise, we stop (reply to the user)
    return END


#######################################
# Build Workflow
#######################################
def get_exercise_chat_agent():
    """Returns the exercise chat agent"""    

    agent_builder = StateGraph(MessagesState)

    # Add nodes
    agent_builder.add_node("llm_call", llm_call)
    agent_builder.add_node("tool_node", tool_node)

    # Add edges to connect nodes
    agent_builder.add_edge(START, "llm_call")
    agent_builder.add_conditional_edges(
        "llm_call",
        should_continue,
        ["tool_node", END]
    )
    agent_builder.add_edge("tool_node", "llm_call")

    # Compile the agent
    agent = agent_builder.compile()
    
    return agent


"""
#######################################
# Run the Model
#######################################
from langchain_core.messages import HumanMessage

agent=get_exercise_chat_agent()
messages = [HumanMessage(content="I want to exercise today.")]
messages = agent.invoke({"messages": messages})
for m in messages["messages"]:
    m.pretty_print()
"""