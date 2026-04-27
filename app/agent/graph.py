from langgraph.graph import StateGraph, END
from app.agent.state import AgentState
from app.agent.nodes import agent_node, escalation_evaluation_node, tools
from langgraph.prebuilt import ToolNode

workflow = StateGraph(AgentState)

workflow.add_node("agent", agent_node)
workflow.add_node("evaluate_escalation", escalation_evaluation_node)
workflow.add_node("tools", ToolNode(tools))

def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    if "speak to a human?" in last_message.content:
        return "evaluate_escalation"
    return END

workflow.set_entry_point("agent")
workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent")
workflow.add_edge("evaluate_escalation", END)

app_graph = workflow.compile()
