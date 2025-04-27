from datetime import datetime
from pydantic import BaseModel


class SessionMessageDTO(BaseModel):
    """
    DTO for session messages.
    """

    id: int
    role: str
    content: str
    created_at: datetime
