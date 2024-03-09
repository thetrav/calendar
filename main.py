from dataclasses import dataclass
from google_calendar import get_calendars, test_data, load_google_creds
from layout import layout_calendars
from model import Surface
from qr import make_qr_code
from datetime import datetime
import json

from env import filter, SERVER_ADDRESS


def hardware_render(image):
    from waveshare_epd import epd12in48b
    from PIL import Image

    try:
        epd = epd12in48b.EPD()
        epd.Init()
        Redimage = Image.new("1", (epd12in48b.EPD_WIDTH, epd12in48b.EPD_HEIGHT), 255)
        epd.display(image, Redimage)
        epd.EPD_Sleep()

    except IOError as e:
        print(f"error: {e}")

    except KeyboardInterrupt:
        print("ctrl + c:")
        epd12in48b.epdconfig.module_exit()
        exit()


def local_render(image):
    image.show("test")


def load_image(load_creds, surface):
    last_render = None
    with open("/tmp/ecalendar-last-render.json") as f:
        last_render = f.read()
    creds = load_creds()
    if not creds or not creds.valid:
        with open("/tmp/ecalendar-last-render.json", "w") as f:
            f.write("credentials")
        if last_render == "credentials":
            return
        return make_qr_code(SERVER_ADDRESS, surface)
    else:
        calendars = get_calendars(creds, filter)
        data_json = json.dumps(calendars)
        if last_render == data_json:
            return
        with open("/tmp/ecalendar-last-render.json", "w") as f:
            f.write(data_json)
        return layout_calendars(calendars, surface)


def run(render, load_creds, width, height):
    surface = Surface(0, 0, width, height)
    image = load_image(load_creds, surface)
    if image is None:
        print("no update")
    else:
        print("updating")
        render(image)


@dataclass
class FakeCreds:
    valid: bool


def fake_creds():
    return FakeCreds(valid=True)


if __name__ == "__main__":
    print("running: " + datetime.now().isoformat())
    # run(local_render, load_google_creds, 1304, 984)

    run(hardware_render, fake_creds, 1304, 984)
