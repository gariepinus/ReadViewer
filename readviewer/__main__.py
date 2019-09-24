import sys
import json
from readviewer.models import Book

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

    books = []
    for book in export_data['books']:
        books.append(Book(book))
    
