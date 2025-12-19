import message_handler as mh
import asyncio
import display
import configparser



async def main():
    # Read config file
    config = configparser.ConfigParser()
    config.read('./config.cfg')
    try:
        api_id = int(config['TelegramClient']['api_id'])
        api_hash = config['TelegramClient']['api_hash']
        source = int(config['TelegramClient']['source'])
        shutdown_query = config['TelegramClient']['shutdown_query']
        message_pattern = config['TelegramClient']['message_pattern']
    except:
        exit('Wrong config format')

    # Setup raspberry lcd display timer
    shutdown_timer = display.ShutdownTimer()

    # Start timer 
    asyncio.create_task(shutdown_timer.display_time_remaining())


    # Request for shutdown scheduler
    async for shutdown_schedule in mh.get_shutdown_periods(api_id,api_hash,source,shutdown_query,message_pattern):
        shutdown_timer.set_schedule(shutdown_schedule)




if __name__ =="__main__":
    asyncio.run(main())