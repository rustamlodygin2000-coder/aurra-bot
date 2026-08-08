import asyncio
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import uvicorn

# === ТОКЕН БОТА ===
BOT_TOKEN = "8955747717:AAF55clB0i20xm0z3eU5lIl52hF-yqYYC6g"

app = FastAPI()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

templates = Jinja2Templates(directory="templates")

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    web_app_url = os.getenv "https://aurra-bot-2.onrender.com"
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🔥 Оценить фото", 
            web_app=WebAppInfo(url=web_app_url)
        )]
    ])
    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        "Добро пожаловать в анонимную оценку внешности.\n"
        "Жми кнопку ниже, чтобы оценивать других!",
        reply_markup=kb
    )

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

async def main():
    asyncio.create_task(dp.start_polling(bot))
    port = int(os.getenv("PORT", 8000))
    config = uvicorn.Config(app, host="0.0.0.0", port=port)
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())


