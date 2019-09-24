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
        self.timestamp = datetime.fromtimestamp(int(str(json_data['timestamp'])[:-3]))

    @property
    def pages(self):
        return self.end_page - self.start_page

    @property
    def progress(self):
        return int((self.end_position - self.start_position) * 100)

    @property
    def speed(self):
        """Pages per hour (integer)"""
        return int(self.pages / (self.duration.seconds / 60 / 60))

    def set_score(self, score):
        self.score = score

    def __str__(self):
        return "{}: {:>4}  - {:>4} ({:>3} pages, {:>3}%), {:>2} pages/hour, {} [{:>2}]".format(self.timestamp, self.start_page, self.end_page, self.pages, self.progress, self.speed, self.duration, self.score)


class Book:

    def __init__(self, json_data):
        self.title = json_data['title']
        self.state = json_data['state']
        self.current_position_timestamp = datetime.fromtimestamp(int(str(json_data['current_position_timestamp'])[:-3]))
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
        return reduce(lambda a,b: a + b.duration, self.sessions, timedelta())

    @property
    def speed(self):
        """Average speed over all sessions."""
        return int(mean([session.speed for session in self.sessions]))

    @property
    def score(self):
        """Average score over all sessions."""
        return int(mean([session.score for session in self.sessions]))

    @property
    def progress(self):
        """Current reading progress."""
        return int(self.current_position * 100)

    @property
    def stats(self):
        """String containing this books stats."""
        return "{page_count} Pages. Progress: {progress}%. Score: {score}.\nRead {duration} in {sessions} Sessions. Average speed: {speed} pages/hour.".format(page_count=self.page_count, progress=self.progress, score=self.score, duration=self.duration, sessions=len(self.sessions), speed=self.speed)

    def __str__(self):
        return "{}. {}.".format(self.title, self.author)
