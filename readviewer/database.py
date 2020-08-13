import json
from readviewer.console_arguments import CONSOLE_ARGUMENTS as args
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from readviewer.models import Base, Reading_Session, Book


engine = create_engine('sqlite:///:memory:', echo=args.verbose)
Session = sessionmaker(bind=engine)
session = Session()


def load(file):
    """Load ReadTracker export data into in-memory-only SQLite database."""
    global engine, session
    Base.metadata.create_all(engine)

    with open(file, "r") as export_file:
        export_data = json.load(export_file)

    for book in export_data['books']:
        new_book = Book(book)
        session.add(new_book)
        session.commit()

        for reading_session in book['sessions']:
            session.add(Reading_Session(reading_session, new_book.id))
        session.commit()
