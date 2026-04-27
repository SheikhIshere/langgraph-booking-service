from langchain_groq import ChatGroq
from app.core.config import settings
from app.agent.tools import search_available_properties, get_listing_details, create_booking
from app.agent.state import AgentState
from langchain_core.messages import SystemMessage, AIMessage
from .prompt import SYSTEM_PROMPT

llm = ChatGroq(api_key=settings.GROQ_API_KEY, model_name="llama-3.3-70b-versatile")
tools = [search_available_properties, get_listing_details, create_booking]
llm_with_tools = llm.bind_tools(tools)

async def agent_node(state: AgentState):
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    response = await llm_with_tools.ainvoke(messages)
    return {"messages": [response]}

async def escalation_evaluation_node(state: AgentState):
    last_user_message = state["messages"][-1].content.lower()
    escalation_status = state.get("escalation_status", "none")
    
    if len(state["messages"]) >= 2:
        prev_ai_message = state["messages"][-2]
        if isinstance(prev_ai_message, AIMessage) and "speak to a human?" in prev_ai_message.content:
            if any(word in last_user_message for word in ["yes", "sure", "okay", "yep", "please"]):
                escalation_status = "escalated"
            elif any(word in last_user_message for word in ["no", "nope", "not now"]):
                escalation_status = "none"
                
    return {"escalation_status": escalation_status}
