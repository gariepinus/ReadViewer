import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from readviewer.models import Base, Reading_Session, Book


engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


def load(file):
    """Load ReadTracker export data into in-memory-only SQLite database."""
    global engine, session
    Base.metadata.create_all(engine)

    with open(file, "r") as data_file:
        export_data = json.load(data_file)

    for book in export_data['books']:
        session.add(Book(book))
        for reading_session in book['sessions']:
            session.add(Reading_Session(reading_session, book['page_count']))

    session.commit()
