from pydantic import BaseModel

class GameIdent(BaseModel):
    game_id: int
    game_name: str


class GameInfo(BaseModel):
    game_name: str
    army: dict | None = None
    resources: dict | None = None
    houses: list | None = None

class GameCreate(GameInfo, GameIdent):
    pass
