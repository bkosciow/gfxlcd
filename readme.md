What it is
===

Library for graphical LCDs for Python on Raspberry Pi. Creates a united interface for supported devices

Supported:

- ili325 via GPIO
- ssd1306 via SPI
- nju6450 via GPIO

On NJU and SSD uses buffer to keep current content as help for page operations.

Wiring is below


Initialization
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
    }
    o = SSD1306(128, 64, drv)
    o.init()
    
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
    }
    o = ILI9325(240, 320, drv)
    o.init()


Drawing functions
===
draw_pixel(x, y)

draw_line(from_x, from_y, to_x, to_y)

draw_rect(x1, y1, x2, y2)

draw_circle(x1, y1, radius)

draw_arc(x1, y1, radius, from_angle, to_angle

fill_rect(x1, y1, x2, y2)


Colours
===
lcd.color = (r, g, b)
lcd.background_color = (r, g ,b)


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
    CS    ------------------------ GND (always selected)
    REST  ------------------------ G25
    LED_A ------------------------ 3.3