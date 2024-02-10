from google_calendar import get_calendars, test_data, load_google_creds
from layout import layout_calendars
from model import Surface
from qr import make_qr_code

AUTH_URL = "https://localhost:8080/calendar_auth"

filter = {
    "bethskurrie@gmail.com": "Beth",
    "the.trav@gmail.com": "Trav",
    "15toskvvqv2uetsil1irv5l2rs@group.calendar.google.com": "B & T",
    "a6fo3oaslp3kvriuiqhpuloij4@group.calendar.google.com": "POPS",
}


def hardware_render(image):
    from waveshare_epd import epd7in3g

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


def local_render(image):
    image.show("test")


def run(render):
    surface = Surface()
    creds = load_google_creds()
    if not creds or not creds.valid:
        image = make_qr_code(AUTH_URL, surface)

        render(image)
    else:
        # calendars = test_data()
        calendars = get_calendars(creds, filter)
        image = layout_calendars(calendars, surface)
        render(image)


run(local_render)
