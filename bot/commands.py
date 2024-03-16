from .admin import auth
from pyrogram import Client
from pyrogram import filters
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
async def start(bot, update, cb=False):
    
    # authorising
    if not auth(update.from_user.id):
        return
    
    text=START_TEXT.format(update.from_user.mention)
    if cb:
        await update.message.edit_text(
            text=text,
            reply_markup=START_BUTTONS,
            disable_web_page_preview=True
        )
    else:
        await update.reply_text(
            text=text,
            disable_web_page_preview=True,
            reply_markup=START_BUTTONS,
            quote=True
        )


@Client.on_message(filters.private & filters.command(["help"]))
async def help(bot, update, cb=False):
    
    # authorising
    if not auth(update.from_user.id):
        return
    
    if cb:
        await update.message.edit_text(
            text=HELP_TEXT,
            reply_markup=HELP_BUTTONS,
            disable_web_page_preview=True
        )
    else:
        await update.reply_text(
            text=HELP_TEXT,
            reply_markup=HELP_BUTTONS,
            disable_web_page_preview=True,
            quote=True
        )


@Client.on_message(filters.private & filters.command(["about"]))
async def about(bot, update, cb=False):
    
    # authorising
    if not auth(update.from_user.id):
        return
    
    if cb:
        await update.message.edit_text(
            text=ABOUT_TEXT,
            reply_markup=ABOUT_BUTTONS,
            disable_web_page_preview=True
        )
    else:
        await update.reply_text(
            text=ABOUT_TEXT,
            reply_markup=ABOUT_BUTTONS,
            disable_web_page_preview=True,
            quote=True
        )
