from aiogram import BaseMiddleware
from aiogram.types import Message
import time

SPAM_DELAY = 0.7

class AntiSpamMiddleware(BaseMiddleware):
    last_time = {}

    async def __call__(self, handler, event: Message, data):
        user = event.from_user.id
        now = time.time()

        if user in self.last_time and now - self.last_time[user] < SPAM_DELAY:
            return

        self.last_time[user] = now
        return await handler(event, data)
