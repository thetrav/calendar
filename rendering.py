from PIL import Image, ImageDraw, ImageFont
from dataclasses import dataclass, field
from model import Surface
from google_calendar import CalendarDay, Event

FONT_SIZE_H1 = 24
FONT_SIZE_SUMMARY = 12
PADDING = 5

BLACK = 0x000000  #   00  BGR
WHITE = 0xFFFFFF  #   01
YELLOW = 0x00FFFF  #   10
RED = 0x0000FF  #   11

DEFAULT_FONT_FILE = "Font.ttc"

weekdays = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


def font(file=DEFAULT_FONT_FILE, size=FONT_SIZE_SUMMARY):
    return ImageFont.truetype(file, size)


@dataclass
class Text:
    text: str
    color: int = BLACK
    font: object = font()

    def render(self, draw: ImageDraw, surface: Surface):
        draw.text(
            (surface.left, surface.top), self.text, font=self.font, fill=self.color
        )


@dataclass
class Box:
    padding: int = PADDING
    margin: int = 0
    stroke: int = 1
    outline: int = None
    horizontal: bool = True
    fill: int = None
    children: list = field(default_factory=list)

    def render(self, draw: ImageDraw, surface: Surface):
        t = surface.top
        b = surface.bottom
        h = b - t
        l = surface.left
        r = surface.right
        w = r - l

        m = self.margin
        p = self.padding

        if self.stroke > 0:
            border = (l + m, t + m, r - m, b - m)
            draw.rectangle(
                border, fill=self.fill, outline=self.outline, width=self.stroke
            )

        nc = len(self.children)
        for i, child in enumerate(self.children):
            cl = l + m + p
            cr = r - m - p
            ct = t + m + p
            cb = b - m - p
            if self.horizontal:
                step = (w - (m + p) * 2) / nc
                cl = l + m + p + int(step * i)
                cr = l + m + p + int(step * (i + 1))
            else:
                step = (h - (m + p) * 2) / nc
                ct = t + m + p + int(step * i)
                cb = t + m + p + int(step * (i + 1))
            cs = Surface(top=ct, left=cl, right=cr, bottom=cb)
            child.render(draw, cs)


def layout_calendars(calendars: list[CalendarDay], surface):
    image = Image.new(
        "RGB", (surface.right, surface.bottom), surface.WHITE
    )  # 255: clear the frame
    draw = ImageDraw.Draw(image)
    box = Box(padding=5)
    h1_font = font(size=FONT_SIZE_H1)
    for day in calendars:
        day_box = Box(padding=5, outline=BLACK, horizontal=False)
        day_box.children.append(
            Text(f"{weekdays[day.date.weekday()]} {day.date.isoformat()}", font=h1_font)
        )
        for event in day.whole_day_events:
            day_box.children.append(
                Box(
                    padding=5,
                    outline=RED,
                    horizontal=False,
                    children=[Text(f"{event.owner}\n    {event.summary}")],
                )
            )
        for event in day.timed_events:
            day_box.children.append(
                Box(
                    padding=5,
                    horizontal=False,
                    outline=RED,
                    children=[
                        Text(
                            f"{event.owner}\n{event.start_time.hour}:{event.start_time.minute}\n    {event.summary}"
                        )
                    ],
                )
            )

        box.children.append(day_box)

    box.render(draw, surface)

    # draw.text((5, 0), 'hello beth', font = font, fill = surface.RED)

    # draw.line((5, 170, 80, 245), fill = surface.RED)
    # draw.line((80, 170, 5, 245), fill = surface.YELLOW)
    # draw.rectangle((5, 170, 80, 245), outline = surface.BLACK)
    # draw.rectangle((90, 170, 165, 245), fill = surface.YELLOW)
    # draw.arc((5, 250, 80, 325), 0, 360, fill = surface.BLACK)
    # draw.chord((90, 250, 165, 325), 0, 360, fill = surface.RED)
    return image
