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


def find_break_index(line, font, pixel_width):
    i = len(line) - 1
    while i > 0:
        length = font.getlength(line[:i])
        if length > pixel_width:
            i -= 1
            continue

        return find_nearest_separator(line, i)
    return 1


def find_nearest_separator(line, max):
    i = max
    while i > 0:
        if line[i] == " ":
            return i
        i -= 1
    return max


def split_line(lines, line, font, pixel_width):
    length = font.getlength(line)

    if length <= pixel_width:
        lines.append(line)
        return
    break_index = find_break_index(line, font, pixel_width)
    lines.append(line[:break_index])
    split_line(lines, line[break_index:], font, pixel_width)


@dataclass
class Text:
    text: str
    _wrapped_text = ""
    color: int = BLACK
    font: object = font()

    def render(self, draw: ImageDraw, surface: Surface):
        text = self.wrapped_text(surface.right - surface.left)
        draw.text((surface.left, surface.top), text, font=self.font, fill=self.color)

    def wrapped_text(self, width):
        if self._wrapped_text != "":
            return self._wrapped_text
        lines = []
        for line in self.text.split("\n"):
            split_line(lines, line, self.font, width)
        self._wrapped_text = "\n".join(lines)
        return self._wrapped_text

    def height(self, width: int):
        _, _, _, height = self.font.getbbox(self.text)
        lines = len(self.wrapped_text(width).split("\n"))
        h = lines * (height + 4)

        return h


@dataclass
class StackChildrenBox:
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
        l = surface.left
        r = surface.right

        m = self.margin
        p = self.padding

        if self.stroke > 0:
            border = (l + m, t + m, r - m, b - m)
            draw.rectangle(
                border, fill=self.fill, outline=self.outline, width=self.stroke
            )

        t = t + m + p
        for child in self.children:
            cl = l + m + p
            cr = r - m - p
            cw = cr - cl
            ch = child.height(cw)
            cb = t + ch
            if cb > b:
                cb = b
            cs = Surface(top=t, left=cl, right=cr, bottom=cb)
            child.render(draw, cs)
            t = t + ch
            if cb == b:
                return


@dataclass
class EqualChildrenBox:
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


@dataclass
class SingleChildBox:
    padding: int = PADDING
    margin: int = 0
    stroke: int = 1
    outline: int = None
    horizontal: bool = True
    fill: int = None
    child: object = None

    def render(self, draw: ImageDraw, surface: Surface):
        t = surface.top
        b = surface.bottom
        l = surface.left
        r = surface.right

        m = self.margin
        p = self.padding
        s = self.stroke

        if self.stroke > 0:
            border = (l + m, t + m, r - m, b - m)
            draw.rectangle(
                border, fill=self.fill, outline=self.outline, width=self.stroke
            )

        child = self.child
        cl = l + m + p + s
        cr = r - m - p - s
        ct = t + m + p + s
        cb = b - m - p - s
        cs = Surface(top=ct, left=cl, right=cr, bottom=cb)
        child.render(draw, cs)

    def height(self, width: int):
        return (
            self.child.height(
                width - (self.margin * 2) - (self.padding * 2) - (self.stroke * 2)
            )
            + self.margin * 2
            + self.padding * 2
            + self.stroke * 2
        )


def layout_calendars(calendars: list[CalendarDay], surface):
    image = Image.new(
        "RGB", (surface.right, surface.bottom), surface.BLACK
    )  # 255: clear the frame
    draw = ImageDraw.Draw(image)
    box = EqualChildrenBox(padding=5, stroke=0)
    h1_font = font(size=FONT_SIZE_H1)
    for day in calendars:
        day_box = StackChildrenBox(padding=5, stroke=0, horizontal=False)
        day_box.children.append(
            Text(
                f"{weekdays[day.date.weekday()]} {day.date.isoformat()}",
                font=h1_font,
                color=WHITE,
            ),
        )

        for event in day.whole_day_events:
            day_box.children.append(
                SingleChildBox(
                    fill=WHITE,
                    margin=2,
                    child=Text(f"{event.owner}\n    {event.summary}"),
                )
            )
        for event in day.timed_events:
            day_box.children.append(
                SingleChildBox(
                    fill=WHITE,
                    margin=2,
                    child=Text(
                        f"{event.owner}\n{event.start_time.hour}:{event.start_time.minute}\n    {event.summary}"
                    ),
                )
            )

        box.children.append(day_box)

    # spacing = 20
    # for i in range(int(480 / spacing)):
    #     t = i * spacing - 1
    #     b = i * spacing
    #     r = (380, t, 390, b)
    #     draw.rectangle(r, RED)

    box.render(draw, surface)

    # draw.text((5, 0), 'hello beth', font = font, fill = surface.RED)

    # draw.line((5, 170, 80, 245), fill = surface.RED)
    # draw.line((80, 170, 5, 245), fill = surface.YELLOW)
    # draw.rectangle((5, 170, 80, 245), outline = surface.BLACK)
    # draw.rectangle((90, 170, 165, 245), fill = surface.YELLOW)
    # draw.arc((5, 250, 80, 325), 0, 360, fill = surface.BLACK)
    # draw.chord((90, 250, 165, 325), 0, 360, fill = surface.RED)
    return image
