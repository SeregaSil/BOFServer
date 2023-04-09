from sqlalchemy import select, delete, update
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from schemas.user import UserCreate, UserUpdate
from models.user import User, UserCode
from core.security import bcrypt_password, generate_user_code
from tasks.worker import send_email_code


async def create(request: UserCreate, db: AsyncSession):
    new_user = User(
        email=request.email, password=bcrypt_password(request.password))
    try:
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Email {request.email} is already used!")
    await create_user_code(new_user, db)


async def get_by_id(id: int, db: AsyncSession):
    user = await db.get(entity=User, ident=id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not available")
    return user


async def get_by_email(email: str, db: AsyncSession):
    try:
        query = (
            select(User).
            where(User.email == email)
        )
        user = (await db.execute(query)).scalars().one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid email")
    return user


async def get_code_by_user_id(id: int, db: AsyncSession):
    code = await db.get(entity=UserCode, ident=id)
    if not code:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Your account already confirm")
    return code.code


async def confirm_user_register(id: int, code: str, db: AsyncSession):
    res = await delete_user_code(id, code, db)
    query = (
        update(User).
        where(User.user_id == res).
        values(is_registered=True)
    )
    await db.execute(query)
    await db.commit()


async def update_user_token(refresh_token: str, id: int, db: AsyncSession):
    query = (
        update(User).
        where(User.user_id == id).
        values(token=refresh_token)
    )
    await db.execute(query)
    await db.commit()


async def delete_user_code(id: int, code: str, db: AsyncSession):
    query = (
        delete(UserCode).
        where(UserCode.user_id == id and UserCode.code == code).
        returning(UserCode.user_id)
    )
    res = (await db.execute(query)).scalars().one()
    return res

async def create_user_code(user: User, db: AsyncSession):
    new_user_code = UserCode(user_id=user.user_id, code=generate_user_code())
    db.add(new_user_code)
    await db.commit()
    send_email_code.delay(user.email, new_user_code.code)
    

async def reset_user_password(request: UserUpdate, db: AsyncSession):
    user = await get_by_email(request.email, db)
    res = await delete_user_code(user.user_id, request.code, db)
    query = (
        update(User).
        where(User.user_id == res).
        values(password=bcrypt_password(request.password))
    )
    await db.execute(query)
    await db.commit()
    
    