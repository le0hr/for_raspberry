from luma.core.interface.serial import spi
from luma.lcd.device import st7789
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime as dt
import asyncio

class Shutdown_timer:
    # Init display object
    def __init__(self) ->None:
        self.serial = spi(
            port=0,          # SPI0
            device=0,        # CS -> GPIO8 (CE0)
            gpio_DC=22,      # DC -> GPIO22
            gpio_RST=27,     # RST -> GPIO27
            bus_speed_hz=1_000_000
        )
        self.device = st7789(
            self.serial,
            width=130,
            height=130,
            h_offset=1,
            v_offset=2,
            rotate=0
        )
        self.img = Image.new("1", (130, 130), 0)   # 0 = чорний
        self.draw = ImageDraw.Draw(self.img)
        self.font = ImageFont.load_default()
                
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
    def time_remaining(self, period: str, is_shuted: bool) -> int:
        # Supportive variable, which helps to find a time difference
        dummy_date = dt.date(dt(1,1,1))
        now = dt.combine(dummy_date, dt.now().time())
        for time in period:
            diff = dt.combine(dummy_date, dt.strptime(time[is_shuted], "%H:%M").time())-now
            diff = diff.total_seconds()       
            if diff >0:
                # Round diff to integer and break down to hours:minutes:seconds format
                diff = round(diff)
                diff_H = diff//3600  
                diff_M = (diff-diff_H*3600)//60
                diff_S = diff-diff_H*3600-diff_M*60
                diff_formated = '{0}:{1}:{2}'.format(diff_H, diff_M, diff_S)
                return diff_formated

    async def display_time_remaining(self, shutdown_schedule:list) ->None:
        while True:
            time_remaining = self.time_remaining(shutdown_schedule, self.is_shuted(shutdown_schedule))
            self.draw.rectangle((0, 0, 129, 129), outline=1)
            self.draw.text((15, 58), "{0}".format(t), fill=1, font=self.font)
            self.device.display(self.img)
            print(time_remaining)
            await asyncio.sleep(1)




