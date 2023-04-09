from pydantic import BaseModel
from schemas.game import GameCreate

class BOFRequest(BaseModel):
    status: int
    detail: str | dict | None = None
    