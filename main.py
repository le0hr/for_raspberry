import messageHandler as mh
import asyncio
from datetime import datetime as dt
from datetime import timedelta as timed


# Сheck if curently in period
def is_shuted(period: str) -> bool:
    now = dt.now().time()
    for i in period:
        start, end = i

        if start == "24:00":
            end_time = dt.time(23, 59, 59)
        else:
            end_time = dt.strptime(end, "%H:%M").time()
            
        start_time = dt.strptime(start, "%H:%M").time()
        if start_time <= now <= end_time:
            return True
    return False

# Calculete the remaining time
def time_remaning(period: str, is_shuted: bool) -> int:
    # Supportive variable, which helps to find a time difference
    dummy_date = dt.date(dt(1,1,1))
    now = dt.combine(dummy_date, dt.now().time())
    for time in period:
        diff = dt.combine(dummy_date, dt.strptime(time[is_shuted], "%H:%M").time())-now
        diff = diff.total_seconds()       
        if diff >0:
            return diff


async def main():
    # Read setup file
    with open('./config.cfg') as file:
        api_id = int(file.readline().removeprefix('api_id='))
        api_hash = file.readline().removeprefix('api_hash=').replace('\r\n', '').replace('\n', '')
        source = int(file.readline().removeprefix('source='))
        shutdown_query = file.readline().removeprefix('shutdown_query=').replace('\r\n', '').replace('\n', '')
        message_pattern = file.readline().removeprefix('message_pattern=').replace('\r\n', '').replace('\n', '')
    async for shutdown_period in mh.get_shutdown_periods(api_id,api_hash,source,shutdown_query,message_pattern):
        print(time_remaning(shutdown_period, is_shuted(shutdown_period)))

# TODO:
# Rework config reading
# Attach an 7-element display to display remaining time
asyncio.run(main())