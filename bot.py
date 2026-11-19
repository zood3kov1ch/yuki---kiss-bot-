import asyncio
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

TOKEN = os.environ.get("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Сюда добавляй сколько угодно своих РП-команд!
RP_COMMANDS = {
    "обнять": ("🫂", "{u} крепко обнял(а) {t}"),
    "поцеловать": ("💋", "{u} нежно поцеловал(а) {t}"),
    "прижать": ("🔥", "{u} прижал(а) {t} к стене"),
    "укусить": ("😈", "{u} ощутимо укусил(а) {t} за шею"),
    "на колени": ("❤️", "{u} усадил(а) {t} к себе на колени"),
    "в душ": ("🚿", "{u} утянул(а) {t} в горячий душ"),
    "уебать": ("👊", "{u} уебал(а) {t} очень жёстко"),
}

@dp.message(F.text.startswith("."))
async def rp_handler(message: Message):
    cmd = message.text[1:].strip().lower()

    if cmd not in RP_COMMANDS:
        return

    if not message.reply_to_message:
        await message.reply("Ответь этой командой на сообщение человека!")
        return

    emoji, template = RP_COMMANDS[cmd]
    user = message.from_user.mention_html()
    target = message.reply_to_message.from_user.mention_html()

    text = f"{emoji} | {template.format(u=user, t=target)}"
    await message.answer(text, parse_mode="HTML")

# Мини-сервер, чтобы Render видел, что бот живой
async def handle_ping(request):
    return web.Response(text="Yuki bot is alive!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

async def main():
    await start_web_server()
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
