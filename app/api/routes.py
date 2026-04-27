from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.api_models import ChatRequest, ChatResponse, HistoryResponse, MessageOut
from app.crud import conversation as crud_conv
from app.agent.graph import app_graph
from langchain_core.messages import HumanMessage, AIMessage

router = APIRouter()

@router.post("/chat/{conversation_id}/message", response_model=ChatResponse)
async def send_message(conversation_id: str, request: ChatRequest, db: AsyncSession = Depends(get_db)):
    # 1. Save user message to DB
    await crud_conv.save_message(db, conversation_id, "user", request.message)
    
    # 2. Fetch history
    history_records = await crud_conv.get_history(db, conversation_id)
    history_messages = []
    for rec in history_records:
        if rec.role == "user":
            history_messages.append(HumanMessage(content=rec.content))
        else:
            history_messages.append(AIMessage(content=rec.content))
            
    # 3. Execute graph
    initial_state = {
        "messages": history_messages,
        "escalation_status": "none"
    }
    result_state = await app_graph.ainvoke(initial_state)
    
    # 4. Extract AI response
    ai_message = result_state["messages"][-1].content
    escalation_status = result_state.get("escalation_status", "none")
    
    # 5. Save AI response to DB
    await crud_conv.save_message(db, conversation_id, "assistant", ai_message)
    
    return ChatResponse(
        response=ai_message,
        requires_human=(escalation_status == "escalated")
    )

@router.get("/chat/{conversation_id}/history", response_model=HistoryResponse)
async def get_chat_history(conversation_id: str, db: AsyncSession = Depends(get_db)):
    history_records = await crud_conv.get_history(db, conversation_id)
    messages = [MessageOut(role=rec.role, content=rec.content) for rec in history_records]
    return HistoryResponse(conversation_id=conversation_id, messages=messages)
