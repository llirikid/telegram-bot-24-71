import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message

from config import BOT_TOKEN, ADMIN_IDS
from antispam import AntiSpamMiddleware
from database import init_db, add_user, add_vote, get_stats

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Routers
router_start = Router()
router_admin = Router()
router_vote = Router()


# ---------- START ----------
@router_start.message(commands=["start"])
async def cmd_start(msg: Message):
    await add_user(msg.from_user.id, msg.from_user.username)
    await msg.answer("👋 Привет! Это Школьный Президент BOT v4.0.\n"
                     "Используй /vote Имя_кандидата чтобы проголосовать.")


# ---------- VOTING ----------
@router_vote.message(commands=["vote"])
async def cmd_vote(msg: Message):
    parts = msg.text.split(maxsplit=1)

    if len(parts) < 2:
        return await msg.answer("Использование: /vote ИмяКандидата")

    candidate = parts[1]
    await add_vote(msg.from_user.id, candidate)

    await msg.answer(f"🗳 Твой голос за *{candidate}* учтён!")


# ---------- ADMIN ----------
@router_admin.message()
async def admin_commands(msg: Message):
    if msg.from_user.id not in ADMIN_IDS:
        return

    if msg.text == "/admin":
        await msg.answer("🔐 Админ-панель:\n/stats — статистика голосов")

    elif msg.text == "/stats":
        stats = await get_stats()

        if not stats:
            return await msg.answer("Пока никто не голосовал.")

        text = "📊 Статистика голосов:\n\n"
        for cand, count in stats:
            text += f"• {cand}: {count}\n"

        await msg.answer(text)


async def main():
    await init_db()

    dp.message.middleware(AntiSpamMiddleware())

    dp.include_router(router_start)
    dp.include_router(router_vote)
    dp.include_router(router_admin)

    print("🚀 BOT v4.0 запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
