import telethon as tl
import asyncio
import re
import time

async def get_shutdown_periods(api_id: int, api_hash: str, source: str, shutdown_query: str, message_pattern: str) -> str:
    client = tl.TelegramClient('anon', api_id, api_hash)
    queue = asyncio.Queue()

    # Telegram client activation
    await client.start()
    asyncio.create_task(client.run_until_disconnected())


    @client.on(tl.events.NewMessage(from_users=source, pattern =r"(?s).*{0}".format(message_pattern) ))
    async def handler(event):
        await queue.put(event.message)  # Every new message stores here

    # Message reader
    while client.is_connected():
        msg = await queue.get()
        a = r"(?m)^" + re.escape(shutdown_query) + r".*$"
        shutdown_period = re.search(r"(?m)^" + re.escape(shutdown_query) + r".*$", msg.message)
        shutdown_period = [i.split(' - ') for i in shutdown_period.group(0)[4:].split(', ')]
        yield shutdown_period  # Returns message when schedulers updated
    

    