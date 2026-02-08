from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel

class ConversationHistoryBase(SQLModel):
    user_id: str = Field(index=True) # Unique identifier for the user session or actual user
    message_content: str
    message_type: str # e.g., "user", "bot", "tool_code", "tool_output"
    timestamp: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class ConversationHistoryCreate(ConversationHistoryBase):
    pass

class ConversationHistoryRead(ConversationHistoryBase):
    id: int

class ConversationHistory(ConversationHistoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
