from datetime import timedelta, datetime
from functools import reduce
from statistics import mean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Interval, Float, String, DateTime

Base = declarative_base()


class Reading_Session(Base):

    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True)
    duration = Column(Interval())
    start_position = Column(Float())
    end_position = Column(Float())
    timestamp = Column(DateTime)
    page_count = Column(Integer)

    def __init__(self, json_data, page_count):
        self.duration = timedelta(seconds=json_data['duration_seconds'])
        self.start_position = json_data['start_position']
        self.end_position = json_data['end_position']
        self.timestamp = datetime.fromtimestamp(
            int(str(json_data['timestamp'])[:-3]))
        self.page_count = page_count

    @property
    def start_page(self):
        """First page of session"""
        return int(self.start_position * self.page_count)

    @property
    def end_page(self):
        """Last page of session"""
        return int(self.end_position * self.page_count)

    @property
    def pages(self):
        """Number of pages read"""
        return self.end_page - self.start_page

    @property
    def progress(self):
        """Percantage of pages of book read (integer)"""
        return int((self.end_position - self.start_position) * 100)

    @property
    def speed(self):
        """Pages per hour (integer)"""
        return int(self.pages / (self.duration.seconds / 60 / 60))

    def __repr__(self):
        return """<Session {}>""".format(self.timestamp)

    def __str__(self):
        return ("{}: {:>4}  - {:>4} ({:>3} pages, "
                "{:>3}%), {:>2} pages/hour, {}").format(
                    self.timestamp, self.start_page, self.end_page, self.pages,
                    self.progress, self.speed, self.duration)


class Session_list(list):

    def sort(self, attribute, reverse=False):
        """Sort sessions by attribute"""
        list.sort(self,
                  key=lambda session: getattr(session, attribute),
                  reverse=reverse)

    def average(self, attribute):
        """Return average for given attribute"""

        if attribute == "duration":
            return timedelta(
                seconds=mean([session.duration.seconds
                              for session in self])).total_seconds() / 3600
        elif attribute == "sessions_per_day":
            return len(self) / self.days
        else:
            return int(mean([
                getattr(session, attribute)
                for session in self]))

    def sum(self, attribute):
        """Return sum for given attribute"""

        if attribute == "duration":
            return reduce(lambda a, b: a + b.duration,
                          self, timedelta()).total_seconds() / 3600
        else:
            return sum([getattr(session, attribute)
                        for session in self])

    @property
    def first(self):
        """Chronologically first session"""
        return sorted(self,
                      key=lambda session: session.timestamp,
                      reverse=False)[0]

    @property
    def last(self):
        """Chronologically last session"""
        return sorted(self,
                      key=lambda session: session.timestamp,
                      reverse=True)[0]

    @property
    def start(self):
        """Date of first session"""
        return self.first.timestamp.date()

    @property
    def end(self):
        """Date of last session"""
        return self.last.timestamp.date()

    @property
    def days(self):
        """Number of days between first and last session"""
        d = (self.last.timestamp.date()
             - self.first.timestamp.date()).days
        if d < 1:
            return 1
        else:
            return d

    def __str__(self):
        if len(self) == 0:
            return "No sessions"

        return ("{pages} pages, {duration:.1f} hours in {sessions} sessions "
                "over {days} days between {first_timestamp} and "
                "{last_timestamp}.\n"
                "[Averages: {speed} pages/hour; "
                "{avg_duration:.1f} hours/session; "
                "{avg_sessions:.1f} sessions/day]").format(
                    pages=self.sum("pages"),
                    duration=self.sum("duration"),
                    sessions=len(self),
                    days=self.days,
                    first_timestamp=self.start,
                    last_timestamp=self.end,
                    speed=self.average("speed"),
                    avg_duration=self.average("duration"),
                    avg_sessions=self.average("sessions_per_day"))


class Book(Base, Session_list):

    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String())
    state = Column(String())
    current_position_timestamp = Column(DateTime())
    page_count = Column(Integer())
    author = Column(String())
    current_position = Column(Float())

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

        for session in json_data['sessions']:
            self.append(Reading_Session(session, self.page_count))

    @property
    def progress(self):
        """Current reading progress."""
        return int(self.current_position * 100)

    @property
    def current_page(self):
        """end_page of last session."""
        return self.last.end_page

    def __repr__(self):
        return """<Book "{}">""".format(self.title[:20])

    def __str__(self):
        return ("{title}. {author}. ({progress}%)\n"
                "{session_stats}").format(
            title=self.title,
            author=self.author,
            progress=self.progress,
            session_stats=Session_list.__str__(self))


class Meta_list(list):
    """List of Session_lists"""

    def sort_by_sum(self, attribute, reverse=False):
        """Sort Session_lists by sum of attribute"""
        list.sort(self,
                  key=lambda session_list: session_list.sum(attribute),
                  reverse=reverse)

    def sort_by_average(self, attribute, reverse=False):
        """Sort Session_lists by average of attribute"""
        list.sort(self,
                  key=lambda session_list: session_list.average(
                      attribute),
                  reverse=reverse)


class Book_list(Meta_list):

    def sort(self, attribute, reverse=False):
        """Sort books attribute"""
        list.sort(self,
                  key=lambda book: getattr(book, attribute), reverse=reverse)

    @property
    def finished(self):
        """Finished books."""
        return Book_list(filter(lambda book: book.state == "Finished", self))

    @property
    def unfinished(self):
        """Unfinished books."""
        return Book_list(filter(lambda book: book.state != "Finished", self))

    def __str__(self):
        if len(self) == 0:
            return "No books"
        elif len(self.finished) > 0 and len(self.unfinished) > 0:
            return ("{books} books "
                    "({finished} read, "
                    "{unfinished} unread)").format(
                        books=len(self),
                        finished=len(self.finished),
                        unfinished=len(self.unfinished)
                    )
        elif len(self.finished) > 0:
            return "{} read books".format(len(self))
        else:
            return "{} unread books".format(len(self))
