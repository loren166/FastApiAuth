from pydantic import BaseModel, UUID4, Field
from uuid import uuid4


class User(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    name: str
    password: str
