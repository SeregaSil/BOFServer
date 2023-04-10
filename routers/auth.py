from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from core import jwtoken
from repository import user_rep, get_async_session
from schemas.token import Token
from schemas.user import UserBase, UserCreate, UserAuth, UserUpdate
from schemas import BOFRequest
from core.security import verify_password
from repository.user_rep import create, get_by_email, update_user_token, reset_user_password, create_user_code
from core.oauth2 import get_current_user, get_current_user_by_refresh

router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=Token)
async def login(request: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_async_session)):
    user = await user_rep.get_by_email(request.username, db)
    if not verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")

    tokens = jwtoken.get_all_tokens(data={"email": user.email})
    await update_user_token(tokens['refresh_token'], user.user_id, db)
    return {"access_token": tokens['access_token'], "refresh_token": tokens['refresh_token'], "token_type": "bearer"}


@router.post('/register', response_model=BOFRequest)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_async_session)):
    await create(user, db)
    return BOFRequest(status=status.HTTP_200_OK,
                      detail='User created')


@router.post('/refresh', response_model=Token)
async def refresh_tokens(current_user: UserAuth = Depends(get_current_user_by_refresh), db: AsyncSession = Depends(get_async_session)):
    new_tokens = jwtoken.get_all_tokens(data={"email": current_user.email})
    await update_user_token(new_tokens['refresh_token'], current_user.user_id, db)
    return {"access_token": new_tokens['access_token'], "refresh_token": new_tokens['refresh_token'], "token_type": "bearer"}


@router.post('/confirm', response_model=BOFRequest)
async def confirm_user(code: str, db: AsyncSession = Depends(get_async_session),
                       current_user: UserAuth = Depends(get_current_user)):
    user_code = await user_rep.get_code_by_user_id(current_user.user_id, db)
    if user_code != code:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid code")
    else:
        await user_rep.confirm_user_register(current_user.user_id, user_code, db)
    return BOFRequest(status=status.HTTP_200_OK, detail='Confirmed!')


@router.post('/codereset', response_model=BOFRequest)
async def code_reset_user_password(user: UserBase, db: AsyncSession = Depends(get_async_session)):
    user = await get_by_email(user.email, db)
    await create_user_code(user, db)
    return BOFRequest(status=status.HTTP_200_OK,
                      detail='Reset code sent')


@router.post('/reset', response_model=BOFRequest)
async def reset_password(user: UserUpdate, db: AsyncSession = Depends(get_async_session)):
    await reset_user_password(user, db)
    return BOFRequest(status=status.HTTP_200_OK,
                      detail='Password reseted!')
