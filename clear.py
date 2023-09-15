#!/usr/bin/python
# -*- coding:utf-8 -*-
import logging
from waveshare_epd import epd7in3g

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd7in3g Demo")

    epd = epd7in3g.EPD()   
    logging.info("init")
    epd.init()
    logging.info("Clear")
    epd.Clear()
    logging.info("sleep")
    epd.sleep()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in3g.epdconfig.module_exit()
    exit()
