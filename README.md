# stats3
BME280 and Luma LED script for system and environmental stats display

Based on the use of a 4 pin i2c SSD1306 one colour OLED (at address 0x3c) on <b>Raspbian (Stretch)</b> and a 4 pin i2c BME280 sensor (at address 0x76). If your devices have different i2c addresses, you will need to edit the script appropriately.

Using the example from the Adafruit SSD1306 Library (stats.py) and both extending for further detail, and simplifying greatly with use of the Luma.OLED library.
