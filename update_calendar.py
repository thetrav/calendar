#!/usr/bin/python
# -*- coding:utf-8 -*-
import logging
from PIL import Image,ImageDraw,ImageFont

from waveshare_epd import epd7in3g

logging.basicConfig(level=logging.DEBUG)

FONT_SIZE = 24

try:
    logging.info("epd7in3g Demo")

    epd = epd7in3g.EPD()   
    logging.info("init and Clear")
    epd.init()
    epd.Clear()

    font = ImageFont.truetype('Font.ttc', FONT_SIZE)
    
    # Drawing on the image
    logging.info("1.Drawing on the image...")
    Himage = Image.new('RGB', (epd.width, epd.height), epd.WHITE)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)
    draw.text((5, 0), 'hello beth', font = font, fill = epd.RED)

    draw.line((5, 170, 80, 245), fill = epd.RED)
    draw.line((80, 170, 5, 245), fill = epd.YELLOW)
    draw.rectangle((5, 170, 80, 245), outline = epd.BLACK)
    draw.rectangle((90, 170, 165, 245), fill = epd.YELLOW)
    draw.arc((5, 250, 80, 325), 0, 360, fill = epd.BLACK)
    draw.chord((90, 250, 165, 325), 0, 360, fill = epd.RED)
    epd.display(epd.getbuffer(Himage))
    epd.sleep()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in3g.epdconfig.module_exit()
    exit()
