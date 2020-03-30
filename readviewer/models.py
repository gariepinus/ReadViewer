from datetime import timedelta, datetime
from functools import reduce
from statistics import mean


class Session:

    def __init__(self, json_data, page_count):
        self.duration = timedelta(seconds=json_data['duration_seconds'])
        self.start_position = json_data['start_position']
        self.start_page = int(json_data['start_position'] * page_count)
        self.end_position = json_data['end_position']
        self.end_page = int(json_data['end_position'] * page_count)
        self.timestamp = datetime.fromtimestamp(
            int(str(json_data['timestamp'])[:-3]))

    @property
    def pages(self):
        """Number of pages read"""
        return self.end_page - self.start_page

    @property
    def progress(self):
        """Percantage of pages of book read"""
        return int((self.end_position - self.start_position) * 100)

    @property
    def speed(self):
        """Pages per hour (integer)"""
        return int(self.pages / (self.duration.seconds / 60 / 60))

    def __str__(self):
        return ("{}: {:>4}  - {:>4} ({:>3} pages, "
                "{:>3}%), {:>2} pages/hour, {}").format(
                    self.timestamp, self.start_page, self.end_page, self.pages,
                    self.progress, self.speed, self.duration)


class Book:

    def __init__(self, json_data):
        self.title = json_data['title']
        self.state = json_data['state']
        self.current_position_timestamp = datetime.fromtimestamp(
            int(str(json_data['current_position_timestamp'])[:-3]))
        self.quotes = json_data['quotes']
        self.page_count = json_data['page_count']
        self.author = json_data['author']
        self.current_position = json_data['current_position']

        if 'closing_remark' in json_data.keys():
            self.closing_remark = json_data['closing_remark']
        else:
            self.closing_remark = None

        self.sessions = []
        for session in json_data['sessions']:
            self.sessions.append(Session(session, self.page_count))

    @property
    def duration(self):
        """Summarized duration of all sessions."""
        return reduce(lambda a, b: a + b.duration, self.sessions, timedelta())

    @property
    def average_duration(self):
        """Average duration per session (hours/session)."""
        delta = timedelta(seconds=mean(
            [session.duration.seconds for session in self.sessions]))
        return delta.total_seconds() / 3600

    @property
    def speed(self):
        """Average speed over all sessions."""
        return int(mean([session.speed for session in self.sessions]))

    @property
    def progress(self):
        """Current reading progress."""
        return int(self.current_position * 100)

    @property
    def start_timestamp(self):
        """Timestamp of first reading session."""
        return self.sessions[0].timestamp

    @property
    def days(self):
        """Number of days between start end current timestamp."""
        return (self.current_position_timestamp.date()
                - self.start_timestamp.date()).days

    @property
    def current_page(self):
        """end_page of last session."""
        return self.sessions[-1].end_page

    @property
    def stats(self):
        """String containing this books stats."""
        return ("{current_page} of {page_count} pages "
                "({progress}%).\n"
                "Read {duration:.1f} hours in {sessions} sessions "
                "over {days} days between {start_timestamp} and "
                "{current_position_timestamp}.\n"
                "[Averages: {speed} pages/hour; "
                "{avg_duration:.1f} hours/session; "
                "{avg_sessions:.1f} sessions/day]").format(
                    current_page=self.current_page,
                    page_count=self.page_count,
                    progress=self.progress,
                    duration=self.duration.total_seconds() / 3600,
                    sessions=len(self.sessions),
                    days=self.days,
                    start_timestamp=self.start_timestamp.date(),
                    current_position_timestamp=self.current_position_timestamp.date(),
                    speed=self.speed,
                    avg_duration=self.average_duration,
                    avg_sessions=len(self.sessions) / self.days)

    def __str__(self):
        return "{}. {}.".format(self.title, self.author)
