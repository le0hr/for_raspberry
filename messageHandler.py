import telethon as tl
import asyncio

async def get_shoutdown_time(api_id, api_hash):
    client = tl.TelegramClient('anon', api_id, api_hash)
    queue = asyncio.Queue()

    @client.on(tl.events.NewMessage(outgoing=True))
    async def handler(event):
        await queue.put(event.message)  # every new message stores here

    await client.start()

    client.run_until_disconnected()

    # message reader
    while True:
        msg = await queue.get()
        yield msg  # returns message when asked