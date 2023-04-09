from fastapi import HTTPException
from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from models.game import Game
from schemas.game import GameCreate, GameInfo


async def create_game(request: GameCreate, user_id: int, db: AsyncSession):
    new_game = Game(**request.dict(exclude_unset=True))
    new_game.user_id = user_id
    db.add(new_game)
    await db.commit()
    await db.refresh(new_game)
    return new_game


async def get_game_by_pk(id: int, user_id: int, db: AsyncSession):
    game = await db.get(entity=Game, ident=(id, user_id))
    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Game with the id {id} is not available")
    return game


async def update_game(request: GameInfo, game_id, user_id: int, db: AsyncSession):
    query = (
        update(Game).
        where(Game.game_id == game_id, Game.user_id == user_id).
        values(request.dict(exclude_unset=True))
    )
    await db.execute(query)
    await db.commit()


async def get_all_games_by_userId(user_id: int, db: AsyncSession):
    query = (
        select(Game).
        where(Game.user_id == user_id)
    )
    games = (await db.execute(query)).scalars().all()
    return games
