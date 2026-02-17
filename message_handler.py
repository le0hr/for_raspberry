import telethon as tl
import asyncio
import re
import time

async def get_outage_periods(api_id: int, api_hash: str, source: str, outage_query: str, message_pattern: str) -> str:
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

        match = re.search(r"6\.1:(.*?)(?=\d\.\d:|$)", msg.message)
        queue_content = match.group(1)
        intervals = re.findall(r"(\d{2}:\d{2})\s*[–-]\s*(\d{2}:\d{2})", queue_content)
        outage_period = [list(i) for i in intervals]
        yield outage_period  
    

    