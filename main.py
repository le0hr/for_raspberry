import messageHandler as mh
import asyncio
# read setup file
print(10)
async def main():
    with open('./config.txt') as file:
        api_id = file.readline().split('=')
        api_hash = file.readline().split('=')

        api_id = int(api_id[1])
        api_hash=api_hash[1]
        
    async for shoutdown_time in mh.get_shoutdown_time(api_id, api_hash):
        print(shoutdown_time)
    print(shoutdown_time)


asyncio.run(main())