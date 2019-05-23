import time
import bme280
import smbus2
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
import os
import time
from PIL import ImageFont
import subprocess

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, rotate=0)
port = 1
address = 0x76
bus = smbus2.SMBus(port)

while True:
    calibration_params = bme280.load_calibration_params(bus, address)
    data = bme280.sample(bus, address, calibration_params)
    font_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                'fonts', 'Minecraftia.ttf'))
    font2 = ImageFont.truetype(font_path, 8)
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell = True )
    cmd = "hostname -s | cut -d\' \' -f1"
    host = subprocess.check_output(cmd, shell = True )
    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell = True )
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell = True )
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell = True )
    humidity_string = "%.2f" % data.humidity
    pressure_string = "%.2f" % data.pressure
    temperature_string = "%.2f" % data.temperature

    with canvas(device) as draw:
        draw.text((0, -2), "IP: " + str(IP), fill="white", font=font2)
        draw.text((0, 6), "Host: " + str(host), fill="white", font=font2)
        draw.text((0, 14), str(CPU), fill="white", font=font2)
        draw.text((0, 22), str(MemUsage), fill="white", font=font2)
        draw.text((0, 30), str(Disk), fill="white", font=font2)
        draw.text((0, 38), "Temperature: " + str(temperature_string) + " C", fill="white", font=font2)
        draw.text((0, 46), "Humidity: " + str(humidity_string) + " %", fill="white", font=font2)
        draw.text((0, 54), "Pressure: " + str(pressure_string) + " hPa", fill="white", font=font2)

def main():
    while True:
        stats(device)
        time.sleep(0.5)
