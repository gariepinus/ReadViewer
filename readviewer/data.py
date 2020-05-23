import json
from functools import reduce
from statistics import mean
from datetime import timedelta
from readviewer.models import Session, Session_list, Book

books = []
sessions = Session_list([])


def load(file):
    """Load ReadTracker export data."""
    global books, sessions

    with open(file, "r") as data_file:
        export_data = json.load(data_file)

    for book in export_data['books']:
        books.append(Book(book))

    # Collect the sessions from all books in seperate list
    sessions = Session_list(reduce(lambda a, b: a + b.sessions, books, []))

    # Sort the lists
    sort_books("current_position_timestamp", reverse=True)
    sessions.sort("timestamp", reverse=True)


def finished_books():
    """Return a list of already finished books."""
    global books
    return filter(lambda book: book.state == "Finished", books)


def unfinished_books():
    """Return a list of unfinished books."""
    global books
    return filter(lambda book: book.state != "Finished", books)


def sessions_in_period(start_date=None, end_date=None):
    """Returns a list of the sessions from start and end date."""
    global sessions

    if start_date is None and end_date is None:
        return sessions
    elif start_date is None:
        return list(filter(lambda session: (
            session.timestamp.date() <= end_date.date()), sessions))
    elif end_date is None:
        return list(filter(lambda session: (
            session.timestamp.date() >= start_date.date()), sessions))
    else:
        return list(filter(lambda session: (
            session.timestamp.date() >= start_date.date() and
            session.timestamp.date() <= end_date.date()), sessions))


def cumulate(attribute, start_date=None, end_date=None):
    """Returns the sum of the given attribute for all sessions
    from start to end date."""

    if attribute == "duration":
        return reduce(lambda a, b: a + b.duration,
                      sessions_in_period(start_date=start_date,
                                         end_date=end_date),
                      timedelta())
    else:
        return sum([getattr(session, attribute)
                    for session in sessions_in_period(start_date=start_date,
                                                      end_date=end_date)])


def sort_books(attribute, reverse=False):
    """Sort books list by the given attribute."""
    global books
    books.sort(key=lambda book: getattr(book, attribute), reverse=reverse)
