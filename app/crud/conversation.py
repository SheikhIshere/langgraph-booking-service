from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.tables import Conversation

async def save_message(db: AsyncSession, conversation_id: str, role: str, content: str):
    db_message = Conversation(
        conversation_id=conversation_id,
        role=role,
        content=content
    )
    db.add(db_message)
    await db.commit()
    await db.refresh(db_message)
    return db_message

async def get_history(db: AsyncSession, conversation_id: str):
    result = await db.execute(
        select(Conversation)
        .where(Conversation.conversation_id == conversation_id)
        .order_by(Conversation.created_at)
    )
    return result.scalars().all()
