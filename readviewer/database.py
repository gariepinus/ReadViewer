import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from readviewer.models import Session, Session_list, Book, Book_list


books = Book_list()
sessions = Session_list()

engine = create_engine('sqlite:///:memory:', echo=True)
session = sessionmaker(bind=engine)


def load(file):
    """Load ReadTracker export data into in-memory-only SQLite database."""
    global books, sessions
    global session

    with open(file, "r") as data_file:
        export_data = json.load(data_file)

    for book in export_data['books']:
        books.append(Book(book))
        sessions += Book(book)

    books.sort("current_position_timestamp", reverse=True)
    sessions.sort("timestamp", reverse=True)
