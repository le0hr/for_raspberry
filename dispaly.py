import adafruit_st7789
import gpiozero as gp
from datetime import datetime as dt
import asyncio

class Shutdown_timer:
    # Init display object
    def __init__(self):
        self.display = gp.LEDMultiCharDisplay(gp.LEDCharDisplay(17, 27, 22, 18, 23, 24, 15), 21)
# A=17 B=27 C=22 D=18 E=23 F=24 G=25 l4=21
    def set_schedule(self, shutdown_schedule:str):
        self.schedule = shutdown_schedule
        
    # Сheck if curently in period
    def is_shuted(self, period: str) -> bool:
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
    def time_remaning(self, period: str, is_shuted: bool) -> int:
        # Supportive variable, which helps to find a time difference
        dummy_date = dt.date(dt(1,1,1))
        now = dt.combine(dummy_date, dt.now().time())
        for time in period:
            diff = dt.combine(dummy_date, dt.strptime(time[is_shuted], "%H:%M").time())-now
            diff = diff.total_seconds()       
            if diff >0:
                return diff

    async def display_time_remainig(self):
        while True:
            self.display.source= self.time_remaning(self.schedule, self.is_shuted(self.schedule))
            await asyncio.sleep(60)




