import sys
import json
from functools import reduce
import readviewer.data as data
from readviewer.models import Book
from readviewer.functions import calculate_scores

if __name__ == "__main__":

    #
    # Eval cli arguments and read json data
    #
    usageinfo = "readviewer <PATH>"
    if len(sys.argv) == 2:
        if sys.argv[1] == "help":
            print(usageinfo)
            exit(0)
        else:
            file_path = sys.argv[1]
    else:
        print(usageinfo)
        exit(1)

    with open(file_path, "r") as data_file:
        export_data = json.load(data_file)

    for book in export_data['books']:
        data.books.append(Book(book))
    
    # Collect the sessions from all books in a list and calculate their scores
    data.sessions = reduce(lambda a,b: a + b.sessions, data.books, [])
    calculate_scores()

    data.books.sort(key = lambda book: book.current_position_timestamp, reverse=True)
    data.sessions.sort(key = lambda session: session.timestamp, reverse=True)
