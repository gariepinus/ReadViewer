import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from readviewer.models import Base, Reading_Session, Session_list, Book, Book_list


books = Book_list()
sessions = Session_list()

engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


def load(file):
    """Load ReadTracker export data into in-memory-only SQLite database."""
    global books, sessions
    global engine, session

    Base.metadata.create_all(engine)

    with open(file, "r") as data_file:
        export_data = json.load(data_file)

    for book in export_data['books']:
        books.append(Book(book))
        sessions += Book(book)
        for reading_session in book['sessions']:
            session.add(Reading_Session(reading_session, book['page_count']))

    books.sort("current_position_timestamp", reverse=True)
    sessions.sort("timestamp", reverse=True)
    session.commit()
