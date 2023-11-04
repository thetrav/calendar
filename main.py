from google_calendar import get_calendars, test_data
from layout import layout_calendars
from model import Surface

filter = {
    "bethskurrie@gmail.com": "Beth",
    "the.trav@gmail.com": "Trav",
    "15toskvvqv2uetsil1irv5l2rs@group.calendar.google.com": "B & T",
    "a6fo3oaslp3kvriuiqhpuloij4@group.calendar.google.com": "POPS",
}


def run_on_hardware():
    from waveshare_epd import epd7in3g

    calendars = get_calendars(filter)
    image = layout_calendars(calendars, Surface())
    try:
        epd = epd7in3g.EPD()
        epd.init()
        epd.display(epd.getbuffer(image))
        epd.sleep()

    except IOError as e:
        print(f"error: {e}")

    except KeyboardInterrupt:
        print("ctrl + c:")
        epd7in3g.epdconfig.module_exit()
        exit()


def run_locally():
    calendars = test_data()
    # calendars = get_calendars(filter)
    image = layout_calendars(calendars, Surface())
    image.show("test")


run_on_hardware()
