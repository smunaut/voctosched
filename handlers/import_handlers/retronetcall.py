import re
import logging

from io import StringIO

from ..base import ImportHandler
from fahrplan.datetime import parse_date, parse_time, parse_datetime, parse_duration
from fahrplan.model.conference import Conference
from fahrplan.model.event import Event
from fahrplan.model.schedule import Schedule
from hacks import noexcept
from util import read_input


log = logging.getLogger(__name__)


SPEAKERS = {
    '@laforge':         (1, 'Harald "LaF0rge" Welte'),
    '@tnt':             (2, 'Sylvain "tnt" Munaut'),
}


class RetroNetCallImportHandler(ImportHandler):
    @noexcept(log)
    def run(self):
        # create the conference object
        conference = Conference(
            title              = "RetroNetCall",
            acronym            = "retronetcall",
            day_count          = 1,
            start              = parse_date("2022-11-01"),
            end                = parse_date("2022-11-01"),
            time_slot_duration = parse_duration("00:30")
        )

        schedule = Schedule(conference=conference)
        schedule.add_room("Virtual")

        content = read_input(self.config['path'])
        t = None

        for l in content.splitlines():
            # Parse line
            f = re.split('\t+', l)

            if t is None:
                t = f
                continue
            else:
                row = dict(zip(t, f))

            # Process it
            if row['ID'] == '':
                continue

            speakers = {}
            for s in row['Speakers'].split(','):
                uid, name = SPEAKERS[s]
                speakers[uid] = name

            schedule.add_event(
                1, "Virtual",
                Event(
                    uid               = row['ID'],
                    date              = parse_datetime(row['Date'] + 'T20:00:00'),
                    start             = parse_time("20:00"),
                    duration          = parse_duration("00:30"),
                    slug              = row['Slug'],
                    title             = row['Title'],
                    language          = "en",
                    persons           = speakers,
                    download_url      = f"https://downloads.osmocom.org/videos/retronetcall/{row['Slug']:s}_master.mov",
                    recording_license = "CC-BY-SA"
                ))

        return schedule
