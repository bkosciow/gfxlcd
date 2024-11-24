What it is
===

Library for graphical LCDs for Python on Raspberry Pi. Creates a united interface for supported devices

Supported:

- ili9486 via SPI
- ili9325 via GPIO
- ssd1306 via SPI
- nju6450 via GPIO
- sh1106 via SPI

And for touch panels:

- ad7843 via SPI, uses irq or not
- ad7846/xpt2046

Bonus

- HD44780 emulation (works with CharLCD)


On NJU and SSD uses buffer to keep current content as help for page operations.

Wiring is below

Demos are in demos directory


LCD initialization
===
## SSD1306 
### SPI

    from driver.ssd1306.spi import SPI
    from driver.ssd1306.ssd1306 import SSD1306
    drv = SPI()
    o = SSD1306(128, 64, drv)
    o.init()
    
If you want to set your own pins:

    drv = SPI()
    drv.pins = {
        'RST': 13,
        'DC': 6,
        'CS': None,
    }
    o = SSD1306(128, 64, drv)
    o.init()

or

    drv = SPI(RST=31, CS=3)


You can add point transformation callback, used during flush:

    def transform_ij(lcd, i, j):
        offset_width = lcd.height // 2
        if 0 <= i < offset_width:
            i = i + offset_width
        else:
            i = i - offset_width
    
        return (i,j)


    lcd.xy_callback = transform_ij

## SH1106

Based on SSD1306, has the same functions

### SPI

    from gfxlcd.driver.sh1106.spi import SPI
    from gfxlcd.driver.sh1106.sh1106 import SH1106
    drv = SPI()
    lcd = SH1106(132, 64, drv)

or
  
    lcd = SH1106(132, 64, SPI(CS=21))


## NJU6450
### GPIO
    
    from gfxlcd.driver.nju6450.gpio import GPIO
    from gfxlcd.driver.nju6450.nju6450 import NJU6450
    drv = GPIO()
    o = NJU6450(122, 32, drv)
    o.init()
    
Custom wiring:
    
    from gfxlcd.driver.nju6450.gpio import GPIO
    from gfxlcd.driver.nju6450.nju6450 import NJU6450
    drv = GPIO()
    drv.pins = {
        'A0': 17,
        'E1': 22,
        'E2': 21,
        'D0': 23,
        'D1': 24,
        'D2': 25,
        'D3': 12,
        'D4': 16,
        'D5': 20,
        'D6': 26,
        'D7': 19,
        'RST': 5,
    }
    o = NJU6450(122, 32, drv)
    o.init()

## ILI9325
### GPIO

    from gfxlcd.driver.ili9325.gpio import GPIO
    from gfxlcd.driver.ili9325.ili9325 import ILI9325
    drv = GPIO()
    o = ILI9325(240, 320, drv)
    o.init()
    
Custom pins:
    
    from gfxlcd.driver.ili9325.gpio import GPIO
    from gfxlcd.driver.ili9325.ili9325 import ILI9325
    drv = GPIO()
    drv.pins = {
        'RS': 27,
        'W': 17,
        'DB8': 22,
        'DB9': 23,
        'DB10': 24,
        'DB11': 5,
        'DB12': 12,
        'DB13': 16,
        'DB14': 20,
        'DB15': 21,
        'RST': 25,
        'LED': None,
        'CS': None
    }
    o = ILI9325(240, 320, drv)
    o.init()

## ILI9486
### SPI

    from gfxlcd.driver.ili9486.spi import SPI
    from gfxlcd.driver.ili9486.ili9486 import ILI9486
    drv = SPI()
    o = ILI9486(320, 480, drv)
    o.rotation = 270
    o.init()

Drawing functions
===
draw_pixel(x, y)

draw_line(from_x, from_y, to_x, to_y)

draw_rect(x1, y1, x2, y2)

draw_circle(x1, y1, radius)

draw_arc(x1, y1, radius, from_angle, to_angle

fill_rect(x1, y1, x2, y2)

draw_image(x, y, PIL.Image)

draw_text(x, y, text)

Colours
===
lcd.color = (r, g, b)

lcd.background_color = (r, g ,b)

lcd.threshold = 255 - for images a threshold between black and white (on monochrome)

lcd.transparency_color = [110, 57] #110 - color(s) that are skipped during drawing an image

Fonts
===
Font class implements Font abstract and is a class that has a dictionary with each char:

    (..)
    [0x3C, 0x66, 0x03, 0x03, 0x73, 0x66, 0x7C, 0x00],   # U+0047 (G)
    (..)

There is one font for now, 8x8 and named **Font8x8** and is used by default.

Touch panels
===

## AD7843

Constructor:
    
    AD7843(width, height, (int_pin), (callback), (cs_pin))
    
Can be used with int_pin and cs_pin

    def callback(position):
        print('(x,y)', position)
    
    touch = AD7843(240, 320, 26, callback, 17)
    touch.init()

or without:

    touch = AD7843(240, 320)
    touch.init()

    while True:
        try:
            time.sleep(0.05)
            ret = touch.get_position()
            if ret:
                print(ret[0], ret[1])
    
        except KeyboardInterrupt:
            touch.close()

There is no automatic calibration. It must be done manually.
         
    self.correction = {
        'x': 364,
        'y': 430,
        'ratio_x': 14.35,
        'ratio_y': 10.59
    }
             
Wiring
===

## SSD1306
### SPI
SPI wiring + 2 additional pins. Defaults:

    LCD             Raspberry Pi
    GND   ----------- GND
    +3.3V ----------- +3.3V
    SCL   ----------- G11
    SDA   ----------- G10
    RST   ----------- G13
    D/C   ----------- G6


## NJU6450
### GPIO
Default wiring:

     LCD                          Raspberry Pi
    1 (Vss)  ------- GND
    2 (Vdd)  ------- +5V
    3 (V0)   ---[-\-] 10k
                   \--- GND
    4 (A0)   ---------------------- G17
    5 (E1)   ---------------------- G22
    6 (E2)   ---------------------- G21
    7 (R/W)  ------- GND
    8 (D0)   ---------------------- G23
    9 (D1)   ---------------------- G24
    10 (D2)  ---------------------- G25
    11 (D3)  ---------------------- G12
    12 (D4)  ---------------------- G16
    13 (D5)  ---------------------- G20
    14 (D6)  ---------------------- G26
    15 (D7)  ---------------------- G19
    16 (RST) ------- +5V
    17 (A)   ------- +5V
    18 (K)   ------- GND

## ILI9325
### GPIO
Default:

    TFT                          Raspberry Pi 2B
    
    GND   ------------------------ GND
    Vcc   ------------------------ 3.3
    RS    ------------------------ G27 (data[H]/cmd[L])
    WR    ------------------------ G17 
    RD    ------------------------ 3.3 (never read from screen)
    DB8   ------------------------ G22
    DB9   ------------------------ G23
    DB10  ------------------------ G24
    DB11  ------------------------ G5
    DB12  ------------------------ G12
    DB13  ------------------------ G16
    DB14  ------------------------ G20
    DB15  ------------------------ G21
    CS    ------------------------ GND (always selected) (or connect to GPIO pin)
    REST  ------------------------ G25
    LED_A ------------------------ 3.3 (can be connected to GPIO pin) 

## ILI9486 (Waveshare)
### SPI
Default:

    RPi                    Shield
    G17 ----------------- TP_IRQ
    G24 ----------------- RS
    G25 ----------------- RST
    G9  ----------------- LCD_CS
    G7  ----------------- TP_CS


HD44780 emulation
===

This driver can work with CharLCD and emulate char LCD

    ili_drv = ILIGPIO()
    ili_drv.pins['LED'] = 6
    ili_drv.pins['CS'] = 18
    lcd = ILI9325(240, 320, ili_drv)
    lcd.auto_flush = False
    lcd.rotation = 0

    drv = HD44780(lcd)
    lcd = CharLCD(drv.width, drv.height, drv, 0, 0)
    lcd.init()

    lcd.write('-!Second blarg!')
    lcd.write("-second line", 0, 1)
    lcd.flush()
