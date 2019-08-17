#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
sys.path.append(r'lib')

import signal
import epd2in13b
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

import pyowm

owm = pyowm.OWM('b8c41b16351aec6d923cef6ca06d404b')
city_id = 2757345 # Mountain View, CA, USA

weather_icon_dict = {200 : "6", 201 : "6", 202 : "6", 210 : "6", 211 : "6", 212 : "6",
                     221 : "6", 230 : "6" , 231 : "6", 232 : "6",

                     300 : "7", 301 : "7", 302 : "8", 310 : "7", 311 : "8", 312 : "8",
                     313 : "8", 314 : "8", 321 : "8",

                     500 : "7", 501 : "7", 502 : "8", 503 : "8", 504 : "8", 511 : "8",
                     520 : "7", 521 : "7", 522 : "8", 531 : "8",

                     600 : "V", 601 : "V", 602 : "W", 611 : "X", 612 : "X", 613 : "X",
                     615 : "V", 616 : "V", 620 : "V", 621 : "W", 622 : "W",

                     701 : "M", 711 : "M", 721 : "M", 731 : "M", 741 : "M", 751 : "M",
                     761 : "M", 762 : "M", 771 : "M", 781 : "M",

                     800 : "1",

                     801 : "H", 802 : "N", 803 : "N", 804 : "Y"
}

def main():
    epd = epd2in13b.EPD()
    while True:

        # Get Weather data from OWM
        obs = owm.weather_at_id(city_id)
        location = obs.get_location().get_name()
        weather = obs.get_weather()
        reftime = weather.get_reference_time()
        description = weather.get_detailed_status()
        temperature = weather.get_temperature(unit='fahrenheit')
        humidity = weather.get_humidity()
        pressure = weather.get_pressure()
        clouds = weather.get_clouds()
        wind = weather.get_wind()
        rain = weather.get_rain()
        sunrise = weather.get_sunrise_time()
        sunset = weather.get_sunset_time()

        print("location: " + location)
        print("weather: " + str(weather))
        print("description: " + description)
        print("temperature: " + str(temperature))
        print("humidity: " + str(humidity))
        print("pressure: " + str(pressure))
        print("clouds: " + str(clouds))
        print("wind: " + str(wind))
        print("rain: " + str(rain))
        print("sunrise: " + time.strftime( '%H:%M', time.localtime(sunrise)))
        print("sunset: " + time.strftime( '%H:%M', time.localtime(sunset)))

        try:
            epd = epd2in13b.EPD()
            epd.init()
            print("Clear...")
            epd.Clear()

            print("Drawing")
            ####### Drawing on the Horizontal image
            HBlackimage = Image.new('1', (epd2in13b.EPD_HEIGHT, epd2in13b.EPD_WIDTH), 255)  # 298*126
            HRedimage = Image.new('1', (epd2in13b.EPD_HEIGHT, epd2in13b.EPD_WIDTH), 255)  # 298*126
            drawblack = ImageDraw.Draw(HBlackimage)
            drawred = ImageDraw.Draw(HRedimage)
            font30 = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoMono-Regular.ttf', 30)
            font25 = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoMono-Regular.ttf', 25)
            font15 = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoMono-Regular.ttf', 15)
            datetime = time.strftime("%H:%M %d/%m")

            drawred.rectangle((0, 0, 212, 50 ), fill = 0)
            drawred.rectangle((0, 90, 212, 104), fill = 0)

            drawred.text((55, 2), 'Hello!', font = font30, fill = 1)
            drawred.text((8, 30), 'The time and date is:', font = font15, fill = 1)
            drawblack.text((20, 56), datetime, font = font25, fill = 0)

            epd.display(epd.getbuffer(HBlackimage.rotate(180)), epd.getbuffer(HRedimage.rotate(180)))
            #epd.display(epd.getbuffer(HRedimage.rotate(180)), epd.getbuffer(HBlackimage.rotate(180)))
            time.sleep(2)


            epd.sleep()

        except:
            print('traceback.format_exc():\n%s',traceback.format_exc())
            exit()
# gracefully exit without a big exception message if possible
def ctrl_c_handler(signal, frame):
    print('Goodbye!')
    # XXX : TODO
    #
    # To preserve the life of the ePaper display, it is best not to keep it powered up -
    # instead putting it to sleep when done displaying, or cutting off power to it altogether.
    #
    # epdconfig.module_exit() shuts off power to the module and calls GPIO.cleanup()
    # The latest epd library chooses to shut off power (call module_exit) even when calling epd.sleep()
    # epd.sleep() calls epdconfig.module_exit(), which in turns calls cleanup().
    # We can therefore end up in a situation calling GPIO.cleanup twice
    #
    # Need to cleanup Waveshare epd code to call GPIO.cleanup() only once
    # for now, calling epdconfig.module_init() to set up GPIO before calling module_exit to make sure
    # power to the ePaper display is cut off on exit
    # I have also modified epdconfig.py to initialize SPI handle in module_init() (vs. at the global scope)
    # because slepe/module_exit closes the SPI handle, which wasn't getting initialized in module_init
    epdconfig.module_init()
    epdconfig.module_exit()
    exit(0)

signal.signal(signal.SIGINT, ctrl_c_handler)

if __name__ == '__main__':
    main()
