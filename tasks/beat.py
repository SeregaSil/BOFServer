from asyncio import current_task, get_event_loop
from contextlib import asynccontextmanager
from sqlalchemy import delete, func, extract, and_
from sqlalchemy.ext.asyncio import async_scoped_session
from models.user import User, UserCode
from repository import async_session_maker
from celery.schedules import crontab
from tasks import beat


loop = get_event_loop()


beat.conf.beat_schedule = {
    'add-every-monday-morning': {
        'task': 'tasks.beat.clear_db_from_not_registered_users',
        'schedule': crontab(minute='*/5'),
        'args': None,
    },
}

beat.conf.timezone = 'UTC'


@asynccontextmanager
async def scoped_session():
    scoped_factory = async_scoped_session(
        async_session_maker,
        scopefunc=current_task,
    )
    try:
        async with scoped_factory() as s:
            yield s
    finally:
        await scoped_factory.remove()


async def delete_unregistered_users():
    async with scoped_session() as db:
        query = (
            delete(UserCode).
            where(func.trunc((
                extract('epoch', UserCode.created_at) -
                extract('epoch', func.now())
            ) / (60 * 60 * 24)) + 12 > 0).
            returning(UserCode.user_id)
        )

        res = (await db.execute(query)).scalars().all()
        if res is None:
            return
        else:
            query = (
                delete(User).
                where(and_(User.user_id.in_(res), User.is_registered == False))
            )
        await db.execute(query)
        await db.commit()


@beat.task(queue='beat')
def clear_db_from_not_registered_users():
    loop.run_until_complete(delete_unregistered_users())
