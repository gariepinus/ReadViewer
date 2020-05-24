import json
from readviewer.models import Session, Session_list, Book, Book_list


books = Book_list()
sessions = Session_list()


def load(file):
    """Load ReadTracker export data."""
    global books, sessions

    with open(file, "r") as data_file:
        export_data = json.load(data_file)

    for book in export_data['books']:
        books.append(Book(book))
        sessions += Book(book)

    books.sort("current_position_timestamp", reverse=True)
    sessions.sort("timestamp", reverse=True)
