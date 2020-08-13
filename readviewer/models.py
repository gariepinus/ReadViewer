from datetime import timedelta, datetime
from functools import reduce
from statistics import mean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import (Column, Integer, Interval, Float, String, DateTime,
                        ForeignKey)


Base = declarative_base()


class Reading_Session(Base):

    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True)
    duration = Column(Interval())
    start_position = Column(Float())
    end_position = Column(Float())
    timestamp = Column(DateTime)
    book_id = Column(Integer, ForeignKey('books.id'))
    book = relationship("Book", back_populates="sessions")

    def __init__(self, json_data, book):
        self.duration = timedelta(seconds=json_data['duration_seconds'])
        self.start_position = json_data['start_position']
        self.end_position = json_data['end_position']
        self.timestamp = datetime.fromtimestamp(
            int(str(json_data['timestamp'])[:-3]))
        self.book_id = book

    @property
    def start_page(self):
        """First page of session"""
        return int(self.start_position * self.book.page_count)

    @property
    def end_page(self):
        """Last page of session"""
        return int(self.end_position * self.book.page_count)

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
        return """<Session#{} [Book#{}] {}>""".format(
                    self.id, self.book_id, self.timestamp)

    def __str__(self):
        return ("{}: {:>4}  - {:>4} ({:>3} pages, "
                "{:>3}%), {:>2} pages/hour, {}").format(
                    self.timestamp, self.start_page, self.end_page, self.pages,
                    self.progress, self.speed, self.duration)


class Book(Base):

    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String())
    state = Column(String())
    current_position_timestamp = Column(DateTime())
    page_count = Column(Integer())
    author = Column(String())
    current_position = Column(Float())
    sessions = relationship("Reading_Session")

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

    @property
    def progress(self):
        """Current reading progress."""
        return int(self.current_position * 100)

    @property
    def current_page(self):
        """end_page of last session."""
        return self.last.end_page

    def __repr__(self):
        return """<Book#{} "{}">""".format(self.id, self.title[:20])

    def __str__(self):
        return "{title}. {author}. ({progress}%)".format(
            title=self.title,
            author=self.author,
            progress=self.progress)
