import json
from functools import reduce
from statistics import mean
from readviewer.models import Session, Book


books = []
sessions = []


def load(file):
    """Load ReadTracker export data."""

    global books, sessions

    with open(file, "r") as data_file:
        export_data = json.load(data_file)

    for book in export_data['books']:
        books.append(Book(book))
    
    # Collect the sessions from all books in a list and calculate their scores
    sessions = reduce(lambda a,b: a + b.sessions, books, [])
    calculate_scores()

    # Sort the lists
    books.sort(key = lambda book: book.current_position_timestamp, reverse=True)
    sessions.sort(key = lambda session: session.timestamp, reverse=True)


def calculate_scores():
    """Calculate session scores and save add them to the instances."""

    global sessions

    max_duration = max([session.duration for session in sessions])
    max_pages = max([session.pages for session in sessions])

    one_percent_duration = max_duration / 100
    one_percent_pages = max_pages / 100

    for session in sessions:
        duration_score = session.duration / one_percent_duration
        pages_score = session.pages / one_percent_pages

        session.set_score(int(mean([duration_score, pages_score])))


def sessions_in_period(start_date=None, end_date=None):
    """Returns a list of the sessions between start and end date."""

    global sessions

    if start_date is None and end_date is None:
        return sessions
    elif start_date is None:
        return list(filter(lambda session: (session.timestamp.date() <= end_date.date()), sessions))
    elif end_date is None:
        return list(filter(lambda session: (session.timestamp.date() >= start_date.date()), sessions))
    else:
        return list(filter(lambda session: (session.timestamp.date() >= start_date.date() and session.timestamp.date() <= end_date.date()), sessions))