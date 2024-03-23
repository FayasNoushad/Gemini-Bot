from .admin import auth, add_user
from pyrogram import Client
from .commands import start, help, about, delete_api_cb


@Client.on_callback_query()
async def cb_data(_, message):
    
    # authorising
    if not auth(message.from_user.id):
        return
    
    # adding user to database
    await add_user(message)
    
    if message.data == "home":
        await start(_, message, cb=True)
    elif message.data == "help":
        await help(_, message, cb=True)
    elif message.data == "about":
        await about(_, message, cb=True)
    elif message.data == "confirm_delete_api":
        await delete_api_cb(_, message, confirm=True)
    elif message.data == "cancel_delete_api":
        await delete_api_cb(_, message, confirm=False)
    else:
        await message.message.delete()
