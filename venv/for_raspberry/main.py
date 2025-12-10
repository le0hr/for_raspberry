import telethon as tl

# read setup file
with open('data.txt') as file:
    api_id = file.readline().split('=')
    api_hash = file.readline().split('=')

    print(api_id)

    api_id = int(api_id[1])
    api_hash=api_hash[1]


def print_message(a):
    

client = tl.TelegramClient('anon', api_id, api_hash)



@client.on(tl.events.NewMessage)
async def reader(event):
    return event.raw_text



client.start()
client.run_until_disconnected()