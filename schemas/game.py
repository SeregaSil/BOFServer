from pydantic import BaseModel

class GameIdent(BaseModel):
    game_id: int
    game_name: str


class GameInfo(BaseModel):
    army: dict | None = None
    resources: dict | None = None
    houses: dict | None = None

class GameCreate(GameInfo, GameIdent):
    pass
