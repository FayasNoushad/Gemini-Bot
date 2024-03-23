from .admin import auth, add_user
from .database import db
from .gemini import check_api
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


START_TEXT = """Hello {},
I am a gemini ai bot.

I can generate (text type) answers using your text (question/query) \
and images using the gemini api.

Click help for more..."""

HELP_TEXT = """--**More Help**--

**In Private (text only):**
- Just send me question as text
- I will reply in text form

**In Private (photo only):**
- Just send me photo
- Then reply /ai command to the photo
- I will reply with generated text

**In Private (photo and text):**
- Send me a photo
- Reply text to the photo
- I will reply with generated text


**In Group (text only):**
- Just send me question as text with /ai command
- I will reply with generated text

**In Group (photo only):**
- Just send me photo
- Then reply /ai command to the photo
- I will reply with generated text

**In Group (photo and text):**
- Send me a photo
- Reply /ai command with text to the photo
- I will reply with generated text

--**Other Commands**--

/api: To add your Gemini API Key from [Google AI Studio](https://aistudio.google.com/app/apikey)
/my_api: To get your Gemini API Key
/delete_api: To delete your Gemini API Key
"""

ABOUT_TEXT = """**About Me**

- **Bot :** `Gemini Bot`
- **Developer :** [GitHub](https://github.com/FayasNoushad) | [Telegram](https://telegram.me/FayasNoushad)
- **Source :** [Click here](https://github.com/FayasNoushad/Gemini-Bot)
- **Language :** [Python 3](https://python.org)
- **Library :** [Pyrogram](https://pyrogram.org)"""

START_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Help', callback_data='help'),
            InlineKeyboardButton('About', callback_data='about'),
            InlineKeyboardButton('Close', callback_data='close')
        ],
        [
            InlineKeyboardButton('Feedback', url='https://telegram.me/FayasNoushad')
        ]
    ]
)

HELP_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Home', callback_data='home'),
            InlineKeyboardButton('About', callback_data='about'),
            InlineKeyboardButton('Close', callback_data='close')
        ]
    ]
)

ABOUT_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Home', callback_data='home'),
            InlineKeyboardButton('Help', callback_data='help'),
            InlineKeyboardButton('Close', callback_data='close')
        ]
    ]
)


@Client.on_message(filters.private & filters.command(["start"]))
async def start(bot, message, cb=False):
    
    # authorising
    if not auth(message.from_user.id):
        return
    
    # adding user to database
    await add_user(message)
    
    text=START_TEXT.format(message.from_user.mention)
    if cb:
        await message.message.edit_text(
            text=text,
            reply_markup=START_BUTTONS,
            disable_web_page_preview=True
        )
    else:
        await message.reply_text(
            text=text,
            disable_web_page_preview=True,
            reply_markup=START_BUTTONS,
            quote=True
        )


@Client.on_message(filters.private & filters.command(["help"]))
async def help(bot, message, cb=False):
    
    # authorising
    if not auth(message.from_user.id):
        return
    
    # adding user to database
    await add_user(message)
    
    if cb:
        await message.message.edit_text(
            text=HELP_TEXT,
            reply_markup=HELP_BUTTONS,
            disable_web_page_preview=True
        )
    else:
        await message.reply_text(
            text=HELP_TEXT,
            reply_markup=HELP_BUTTONS,
            disable_web_page_preview=True,
            quote=True
        )


@Client.on_message(filters.private & filters.command(["about"]))
async def about(bot, message, cb=False):
    
    # authorising
    if not auth(message.from_user.id):
        return
    
    # adding user to database
    await add_user(message)
    
    if cb:
        await message.message.edit_text(
            text=ABOUT_TEXT,
            reply_markup=ABOUT_BUTTONS,
            disable_web_page_preview=True
        )
    else:
        await message.reply_text(
            text=ABOUT_TEXT,
            reply_markup=ABOUT_BUTTONS,
            disable_web_page_preview=True,
            quote=True
        )


@Client.on_message(filters.private & filters.command(["api", "add_api"]))
async def add_api(bot, message):
    
    # authorising
    if not auth(message.from_user.id):
        return
    
    # adding user to database
    await add_user(message)
    
    if (" " not in message.text):
        await message.reply_text("Send your Gemini API Key")
        return
    
    api = message.text.split(" ", 1)[1]
    m = await message.reply_text("Checking API Key...")
    if check_api(api):
        await db.update_api(id=message.from_user.id, api=api)
        if await db.get_api(message.from_user.id):
            text = "API Key updated successfully"
        else:
            text = "API Key added successfully"
        await m.edit_text(text)
    else:
        await m.edit_text("Invalid API Key")


@Client.on_message(filters.private & filters.command(["my_api", "get_api"]))
async def get_api(bot, message):
    
    # authorising
    if not auth(message.from_user.id):
        return
    
    # adding user to database
    await add_user(message)
    
    api = await db.get_api(message.from_user.id)
    if api:
        await message.reply_text(f"Your Gemini API Key is\n`{api}`")
    else:
        await message.reply_text("You haven't added your Gemini API Key")


@Client.on_message(filters.private & filters.command(["delete_api", "remove_api"]))
async def delete_api(bot, message):
    
    # authorising
    if not auth(message.from_user.id):
        return
    
    # adding user to database
    await add_user(message)
    
    text = "Are you sure to delete your Gemini API Key?"
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('Yes', callback_data='confirm_delete_api'),
                InlineKeyboardButton('No', callback_data='cancel_delete_api')
            ]
        ]
    )
    await message.reply_text(
        text=text,
        reply_markup=buttons,
        quote=True
    )


# Callbacks
async def delete_api_cb(bot, message, confirm):
    m = message.message
    if confirm:
        await m.edit_text("Deleting your Gemini API Key...")
        if await db.get_api(message.from_user.id):
            await db.update_api(message.from_user.id, None)
            await m.edit_text("API Key removed successfully")
        else:
            await m.edit_text("You haven't added your Gemini API Key")
    else:
        await m.edit_text("Cancelled the process")
