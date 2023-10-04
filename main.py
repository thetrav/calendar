from google_calendar import get_calendars
from rendering import layout_calendars
from model import Surface
   
calendars = []#get_calendars()
image = layout_calendars(calendars, Surface())
image.show("test")