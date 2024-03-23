from .database import db
from vars import AUTH, AUTH_USERS


def auth(id):
    if AUTH:
        if id in AUTH_USERS:
            return True
        else:
            return False
    else:
        return True


async def add_user(message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
    return
