from typing import TypedDict, Annotated, Sequence
import operator
from dotenv import load_dotenv

from langchain_core.messages import BaseMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from tools import tools

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm_with_tools = llm.bind_tools(tools)

def agent_node(state: AgentState):
    sys_prompt = SystemMessage(
        content="You are an AI Assistant with tool access. Always select the appropriate tool when calculation, weather lookup, or knowledge searching is needed."
    )
    response = llm_with_tools.invoke([sys_prompt] + list(state["messages"]))
    return {"messages": [response]}

def should_continue(state: AgentState):
    last_msg = state["messages"][-1]
    if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
        return "tools"
    return END

workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.add_node("tools", ToolNode(tools))

workflow.set_entry_point("agent")
workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
workflow.add_edge("tools", "agent")

agent_app = workflow.compile()
