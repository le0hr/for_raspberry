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
        outage_query = config['TelegramClient']['outage_query']
        message_pattern = config['TelegramClient']['message_pattern']
    except:
        exit('Wrong config format')

    # Setup raspberry lcd display timer
    outage_timer = display.OutageTimer()

    # Start timer 
    asyncio.create_task(outage_timer.display_time_remaining())


    # Request for shutdown scheduler
    async for outage_schedule in mh.get_outage_periods(api_id,api_hash,source,outage_query,message_pattern):
        outage_timer.set_schedule(outage_schedule)




if __name__ =="__main__":
    asyncio.run(main())