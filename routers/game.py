from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.oauth2 import get_current_user
from repository import get_async_session
from repository.game_rep import get_game_by_pk, create_game, update_game, get_all_games_by_userId
from schemas.game import GameInfo, GameCreate, GameIdent
from schemas.user import UserAuth
from schemas import BOFRequest
router = APIRouter(tags=['Game'] ,prefix='/game')


@router.get('/{game_id}', response_model=GameInfo)
async def get_game(game_id: int, db: AsyncSession = Depends(get_async_session),
                   current_user: UserAuth = Depends(get_current_user)):
    game = await get_game_by_pk(game_id, current_user.user_id, db)
    response = GameInfo(**game.__dict__)
    return response


@router.post('', response_model=BOFRequest)
async def create_game_save(game: GameCreate, db: AsyncSession = Depends(get_async_session),
                           current_user: UserAuth = Depends(get_current_user)):
    await create_game(game, current_user.user_id, db)
    return BOFRequest(status=status.HTTP_200_OK, detail='Save created!')


@router.put('/{game_id}', response_model=BOFRequest)
async def put_game(game: GameInfo, game_id: int, db: AsyncSession = Depends(get_async_session),
                   current_user: UserAuth = Depends(get_current_user)):
    await update_game(game, game_id, current_user.user_id, db)
    return BOFRequest(status=status.HTTP_200_OK, detail='Save updated!')


@router.get('', response_model=List[GameIdent])
async def get_all_games_info(db: AsyncSession = Depends(get_async_session),
                        current_user: UserAuth = Depends(get_current_user)):
    games = await get_all_games_by_userId(current_user.user_id, db)
    response: List[GameIdent] = []
    for i in games:
        response.append(GameIdent(game_id=i.game_id, game_name=i.game_name))
    return response
