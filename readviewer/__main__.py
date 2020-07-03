import argparse
import readviewer.database as database
# import readviewer.ui as ui

if __name__ == "__main__":

    #
    # Eval cli arguments
    #
    parser = argparse.ArgumentParser(description="""Visualize
                         ReadTracker data in your terminal.""",
                                     epilog="""ReadTracker by Christoffer
                         Klang: https://github.com/christoffer/readtracker""",
                                     prog="readviewer")
    parser.add_argument('file', metavar='FILE', type=str,
                        help="""the exported
                         JSON data you want to view""")
    args = parser.parse_args()

    #
    # Load json data
    #
    database.load(args.file)

    #
    # Start UI loop
    #
    # ui.run()
