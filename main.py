import messageHandler as mh
import asyncio
import dispaly
import configparser



async def main():
    # Read config file
    config = configparser.ConfigParser()
    config.read('./config.cfg')
    try:
        api_id = int(config['TelegramClient']['api_id'])
        api_hash = config['TelegramClient']['api_hash']
        source = config['TelegramClient']['source']
        shutdown_query = config['TelegramClient']['shutdown_query']
        message_pattern = config['TelegramClient']['message_pattern']
    except:
        exit('Wrong config format')

    # Setup raspberry 7-segment multi-display
    raspberry_display = dispaly.Shutdown_timer()

    # Request for shutdown scheduler
    async for shutdown_scheduler in mh.get_shutdown_periods(api_id,api_hash,source,shutdown_query,message_pattern):
        raspberry_display.display_time_remaining(shutdown_scheduler)



# TODO:
# Rewrite display.py for LCD display
if __name__ =="__main__":
    asyncio.run(main())