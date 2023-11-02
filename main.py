from google_calendar import get_calendars, test_data
from rendering import layout_calendars
from model import Surface

# from waveshare_epd import epd7in3g

calendars = get_calendars()
# calendars = test_data()

image = layout_calendars(calendars, Surface())
image.show("test")

# try:
#     epd = epd7in3g.EPD()
#     epd.init()
#     epd.display(epd.getbuffer(image))
#     epd.sleep()

# except IOError as e:
#     print(f"error: {e}")

# except KeyboardInterrupt:
#     print("ctrl + c:")
#     epd7in3g.epdconfig.module_exit()
#     exit()
