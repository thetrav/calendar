from __future__ import print_function

import datetime
from zoneinfo import ZoneInfo
import os.path
from dataclasses import dataclass, field
from operator import attrgetter

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
TIMEZONE = "Australia/Melbourne"


@dataclass
class GoogleCalendar:
    id: str
    name: str


@dataclass
class Event:
    owner: str
    summary: str
    start_time: datetime.time = None
    end_time: datetime.time = None


@dataclass
class CalendarDay:
    date: datetime.date
    whole_day_events: list[Event] = field(default_factory=list)
    timed_events: list[Event] = field(default_factory=list)


def load_google_creds():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    token_filename = "token.json"
    if os.path.exists(token_filename):
        creds = Credentials.from_authorized_user_file(token_filename, SCOPES)

    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
        except:
            creds = None

    if not creds or not creds.valid:
        # TODO: the device has no input, so we need to replace this with some other flow
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
        with open(token_filename, "w") as token:
            token.write(creds.to_json())
    return creds


def list_google_calendars(creds):
    try:
        service = build("calendar", "v3", credentials=creds)
        result = service.calendarList().list().execute()
        return [GoogleCalendar(c["id"], c["summary"]) for c in result.get("items", [])]
    except HttpError as error:
        print(f"An error occurred: {error}")
        return []


def list_google_events(creds, calendar_id, min, max):
    try:
        service = build("calendar", "v3", credentials=creds)
        # TODO: fix handling of timezone, we don't actually want UTC, we want local time
        events_result = (
            service.events()
            .list(
                calendarId=calendar_id,
                timeMin=min.isoformat(),
                timeMax=max.isoformat(),
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        return events_result.get("items", [])

    except HttpError as error:
        print("An error occurred: %s" % error)
        return []


def add_events_to_calendars(events_from_google, calendar_name, calendars):
    for event in events_from_google:
        start = event["start"]
        start_date = start.get("date", start.get("dateTime"))
        date = datetime.datetime.fromisoformat(start_date).date()
        dest = next((c for c in calendars if c.date == date), None)
        if dest:
            event = Event(owner=calendar_name, summary=event["summary"])
            if "dateTime" in start:
                event.start_time = datetime.datetime.fromisoformat(start["dateTime"])
                dest.timed_events.append(event)
            else:
                dest.whole_day_events.append(event)


def get_calendars():
    creds = load_google_creds()
    google_calendars = list_google_calendars(creds)
    today = datetime.datetime.combine(
        datetime.date.today(), datetime.time.min, tzinfo=ZoneInfo(TIMEZONE)
    )
    tomorrow = today + datetime.timedelta(days=1)
    calendars = [CalendarDay(date=today.date()), CalendarDay(date=tomorrow.date())]
    for gcal in google_calendars:
        events = list_google_events(creds, gcal.id, today, tomorrow)
        add_events_to_calendars(events, gcal.name, calendars)
    for cal in calendars:
        cal.whole_day_events.sort(key=attrgetter("start_time"))
        cal.timed_events.sort(key=attrgetter("start_time"))
    return calendars


def test_data():
    today = datetime.datetime.combine(
        datetime.date.today(), datetime.time.min, tzinfo=ZoneInfo(TIMEZONE)
    )
    tomorrow = today + datetime.timedelta(days=1)
    calendars = [CalendarDay(date=today.date()), CalendarDay(date=tomorrow.date())]
    today = calendars[0]
    tomorrow = calendars[1]
    today.whole_day_events.append(Event("Travis", "Working on calendar epaper thing"))
    today.timed_events.append(
        Event(
            "Travis",
            "Steve coming over",
            datetime.datetime(2023, 11, 2, 11, 30, tzinfo=ZoneInfo(TIMEZONE)),
        )
    )
    event_time = datetime.datetime(2023, 11, 3, 9, tzinfo=ZoneInfo(TIMEZONE))
    for n in range(10):
        tomorrow.timed_events.append(Event("Travis", f"fake event #{n}", event_time))
        event_time = event_time + datetime.timedelta(minutes=30)
    return calendars


if __name__ == "__main__":
    print(f"calendars: {get_calendars()}")
