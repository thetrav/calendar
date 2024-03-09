from dataclasses import dataclass
from google_calendar import get_calendars, test_data, load_google_creds
from layout import layout_calendars
from model import Surface
from qr import make_qr_code
from datetime import datetime

from env import filter, SERVER_ADDRESS


def hardware_render(image):
    from waveshare_epd import epd12in48b

    try:
        epd = epd12in48b.EPD()
        epd.init()
        epd.display(image)
        epd.EPD_Sleep()

    except IOError as e:
        print(f"error: {e}")

    except KeyboardInterrupt:
        print("ctrl + c:")
        epd12in48b.epdconfig.module_exit()
        exit()


def local_render(image):
    image.show("test")


def run(render, load_creds, width, height):
    surface = Surface(0, 0, width, height)
    creds = load_creds()
    if not creds or not creds.valid:
        image = make_qr_code(SERVER_ADDRESS, surface)
        render(image)
    else:
        calendars = test_data()
        # calendars = get_calendars(creds, filter)
        image = layout_calendars(calendars, surface)
        render(image)


@dataclass
class FakeCreds:
    valid: bool


def fake_creds():
    return FakeCreds(valid=True)


if __name__ == "__main__":
    print("running: " + datetime.now().isoformat())
    run(local_render, load_google_creds, 1304, 984)

    run(local_render, fake_creds, 1304, 984)
