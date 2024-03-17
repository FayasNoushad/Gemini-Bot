import os
import pathlib
import textwrap
import PIL.Image
from vars import GEMINI_API
from .admin import auth
from pyrogram import Client, filters
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Feedback', url='https://telegram.me/FayasNoushad')
        ]
    ]
)


def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


@Client.on_message(filters.command(["ai", "genai", "aitext", "gemini", "bard"]))
async def gemini_ai(_, message):

    # authorising
    if not auth(message.from_user.id):
        return
    
    if (message.reply_to_message) and (message.reply_to_message.photo):
        await gemini_ai_img(_, message)
    else:
        # To avoid command only
        if (" " not in message.text):
            return
        await gemini_ai_text(_, message)


@Client.on_message(filters.private & filters.text)
async def gemini_ai_private(_, message):
    
    if message.text.startswith("/"):
        return
    
    # authorising
    if not auth(message.from_user.id):
        return
    
    if (message.reply_to_message) and (message.reply_to_message.photo):
        await gemini_ai_img(_, message)
    else:
        await gemini_ai_text(_, message, text=message.text)


@Client.on_message(filters.command(["genaitext", "aitext", "geminitext", "textai"]))
async def gemini_ai_text(_, message, text=""):
    
    # authorising
    if not auth(message.from_user.id):
        return
    
    # To avoid command only messages
    if message.text.startswith("/") and (" " not in message.text):
        return
    
    m = await message.reply_text("Please wait...", quote=True)
    
    if text:
        query = text
    else:
        if (message.reply_to_message and (" " not in message.text)):
            query = message.reply_to_message.text
        else:
            query = message.text.split(" ", 1)[1]

    genai.configure(api_key=GEMINI_API)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(query)
    
    if response.parts:
        for part in response.parts:
            result = part.text
            await message.reply_text(
                text=result,
                disable_web_page_preview=True,
                reply_markup=BUTTONS,
                quote=True
            )
    else:
        result = to_markdown(response.text)
        await message.reply_text(
            text=result,
            disable_web_page_preview=True,
            reply_markup=BUTTONS,
            quote=True
        )
    await m.delete()


@Client.on_message(filters.command(["aiimage", "genaiimage", "aiimg", "geminivision", "imgai"]))
async def gemini_ai_img(_, message):
    
    # authorising
    if not auth(message.from_user.id):
        return
    
    m = await message.reply_text("Please wait...", quote=True)
    
    image = await message.reply_to_message.download()
    img = PIL.Image.open(image)
    
    genai.configure(api_key=GEMINI_API)
    model = genai.GenerativeModel('gemini-pro-vision')
    
    if (" " in message.text):
        query = message.text.split(" ", 1)[1]
        response = model.generate_content([query, img])
    else:
        response = model.generate_content(img)
    
    if response.parts:
        for part in response.parts:
            result = part.text
            await message.reply_text(
                text=result,
                disable_web_page_preview=True,
                reply_markup=BUTTONS,
                quote=True
            )
    else:
        result = to_markdown(response.text)
        await message.reply_text(
            text=result,
            disable_web_page_preview=True,
            reply_markup=BUTTONS,
            quote=True
        )
    await m.delete()
    os.remove(image)
