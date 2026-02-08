from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from backend.app.db.database import get_session
from backend.app.models.conversation import ConversationHistory, ConversationHistoryCreate, ConversationHistoryRead
from pydantic import BaseModel
from typing import List
import os

router = APIRouter()

class ChatMessage(BaseModel):
    message: str
    user_id: str = "dummy_user"

class ChatResponse(BaseModel):
    response: str
    tasks: List[dict] = []

if os.getenv("IS_TESTING", "False").lower() == "true":
    async def process_message(user_message: str) -> str:
        if "list" in user_message:
            return "AI has listed your tasks:\n- Task 1 (Completed: False)\n- Task 2 (Completed: True)"
        elif "mark" in user_message:
            return "AI has marked task 1 as complete."
        elif "update" in user_message:
            return "AI has updated task 2."
        elif "delete" in user_message:
            return "AI has deleted task 3."
        return f"AI Agent response (mocked for testing) to: '{user_message}'"
else:
    from ai_agent.agent.main import process_message

@router.post("/chat/message", response_model=ChatResponse)
async def chat_message(message: ChatMessage, session: Session = Depends(get_session)):
    user_message_content = message.message
    
    user_entry = ConversationHistory.model_validate(ConversationHistoryCreate(
        user_id=message.user_id,
        message_content=user_message_content,
        message_type="user"
    ))
    session.add(user_entry)
    session.commit()

    ai_response_content = await process_message(user_message_content)

    bot_entry = ConversationHistory.model_validate(ConversationHistoryCreate(
        user_id=message.user_id,
        message_content=ai_response_content,
        message_type="bot"
    ))
    session.add(bot_entry)
    session.commit()
    
    returned_tasks = []
    if "AI has listed your tasks" in ai_response_content:
        lines = ai_response_content.split('\n')
        for line in lines:
            if line.startswith("- "):
                desc_part = line[2:]
                description = desc_part.split(' (Completed:')[0].strip()
                is_completed_str = desc_part.split('(Completed: ')[1].replace(')', '').strip()
                is_completed = (is_completed_str == 'True')
                returned_tasks.append({"description": description, "is_completed": is_completed, "id": 0})
    
    return ChatResponse(response=ai_response_content, tasks=returned_tasks)

@router.get("/chat/history/{user_id}", response_model=List[ConversationHistoryRead])
def get_chat_history(user_id: str, session: Session = Depends(get_session)):
    history = session.exec(select(ConversationHistory).where(ConversationHistory.user_id == user_id).order_by(ConversationHistory.timestamp)).all()
    return history