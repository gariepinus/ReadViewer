import json
from functools import reduce
from readviewer.models import Session, Book

books = []
sessions = []


def load(file):
    with open(file, "r") as data_file:
        export_data = json.load(data_file)

    for book in export_data['books']:
        books.append(Book(book))
    
    # Collect the sessions from all books in a list and calculate their scores
    sessions = reduce(lambda a,b: a + b.sessions, books, [])
    #calculate_scores()

    books.sort(key = lambda book: book.current_position_timestamp, reverse=True)
    sessions.sort(key = lambda session: session.timestamp, reverse=True)
