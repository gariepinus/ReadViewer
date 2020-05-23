import json
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
        sessions += Book(book)

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


def sort_books(attribute, reverse=False):
    """Sort book list by given attribute"""
    global books
    books.sort(key=lambda book: getattr(book, attribute), reverse=reverse)
