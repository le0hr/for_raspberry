from luma.core.interface.serial import spi
from luma.lcd.device import st7789
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime as dt
import asyncio

class OutageTimer:
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

        self.schedule = [['0:00', '0:00']]
                
    def set_schedule(self, outage_schedule:str):
        self.schedule = outage_schedule
        
    # Сheck if curently in period
    def is_shuted(self, period: str) -> bool:
        _now = dt.now().time()
        for i in period:
            _start, _end = i

            if _start == "24:00":
                _end_time = dt.time(23, 59, 59)
            else:
                _end_time = dt.strptime(_end, "%H:%M").time()
                
            _start_time = dt.strptime(_start, "%H:%M").time()
            if _start_time <= _now <= _end_time:
                return True
        return False

    # Calculete the remaining time
    def time_remaining(self, period: str, is_shuted: bool) -> int:
        # Supportive variable, which helps to find a time difference
        _dummy_date = dt.date(dt(1,1,1))
        _now = dt.combine(_dummy_date, dt.now().time())
        for time in period:
            _diff = dt.combine(_dummy_date, dt.strptime(time[is_shuted], "%H:%M").time())-_now
            _diff = _diff.total_seconds()       
            if _diff >0:
                # Round diff to integer and break down to hours:minutes:seconds format
                _diff = round(_diff)
                _diff_H = _diff//3600  
                _diff_M = (_diff-_diff_H*3600)//60
                _diff_S = _diff-_diff_H*3600-_diff_M*60
                _diff_formated = '{0}:{1}:{2}'.format(_diff_H, _diff_M, _diff_S)
                return _diff_formated

    async def display_time_remaining(self) ->None:
        while True:
            _time_remaining = self.time_remaining(self.schedule, self.is_shuted(self.schedule))
            self.draw.rectangle((0, 0, 129, 129), outline=1)
            self.draw.text((15, 58), "{0}".format(_time_remaining), fill=1, font=self.font)
            self.device.display(self.img)
            print(_time_remaining, end = '\r')   
            await asyncio.sleep(1)



