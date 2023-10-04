from PIL import Image,ImageDraw,ImageFont
from dataclasses import dataclass, field
from model import Surface

FONT_SIZE = 24
PADDING = 5

BLACK  = 0x000000   #   00  BGR
WHITE  = 0xffffff   #   01
YELLOW = 0x00ffff   #   10
RED    = 0x0000ff   #   11

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
        h = b-t
        l = surface.left
        r = surface.right
        w = r-l
        
        m = self.margin
        p = self.padding

        if self.stroke > 0:
            border = (l+m, t+m, r-m, b-m)
            draw.rectangle(border, fill = self.fill, outline = self.outline, width=self.stroke)

        nc = len(self.children)
        for i, child in enumerate(self.children):
            cl = l + m + p
            cr = r - m - p
            ct = t + m + p
            cb = b - m - p
            if self.horizontal:
                step = (w-(m+p)*2) / nc
                cl = l + m+p + int(step * i)
                cr = l + m+p + int(step * (i + 1))
            else:
                step = (h-(m+p)*2) / nc
                ct = t + m+p + int(step * i)
                cb = t + m+p + int(step * (i+1))
            cs = Surface(top=ct,left=cl,right=cr,bottom=cb)
            child.render(draw, cs)

def layout_calendars(calendars, surface):
    font = ImageFont.truetype('Font.ttc', FONT_SIZE)
    
    image = Image.new('RGB', (surface.right, surface.bottom), surface.WHITE)  # 255: clear the frame
    draw = ImageDraw.Draw(image)

    box = \
    Box(margin=5, outline=BLACK, children=[
        Box(margin=5, padding=5, fill=RED, outline=BLACK, horizontal=False,
            children=[
                Box(fill=WHITE, outline=BLACK),
                Box(fill=WHITE, outline=BLACK),
            ]),
        Box(margin=5, fill = RED, outline = BLACK, horizontal=False,
            children=[
                Box(fill=WHITE, outline=BLACK),
                Box(fill=BLACK, outline=BLACK),
                Box(fill=YELLOW, outline=BLACK),
                Box(fill=RED, outline=BLACK),
            ])
    ])
    box.render(draw, surface)

    # draw.text((5, 0), 'hello beth', font = font, fill = surface.RED)

    # draw.line((5, 170, 80, 245), fill = surface.RED)
    # draw.line((80, 170, 5, 245), fill = surface.YELLOW)
    # draw.rectangle((5, 170, 80, 245), outline = surface.BLACK)
    # draw.rectangle((90, 170, 165, 245), fill = surface.YELLOW)
    # draw.arc((5, 250, 80, 325), 0, 360, fill = surface.BLACK)
    # draw.chord((90, 250, 165, 325), 0, 360, fill = surface.RED)
    return image