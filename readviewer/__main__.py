import sys
import argparse
import readviewer.data as data
# import readviewer.ui as ui

if __name__ == "__main__":

    #
    # Eval cli arguments
    #
    parser = argparse.ArgumentParser(description="""Visualize
                         ReadTracker data in your terminal.""")
    parser.add_argument('file', metavar='FILE', type=str,
                        help="""the exported
                         JSON data you want to view""")
    args = parser.parse_args()

    #
    # Load json data
    #
    data.load(args.file)

    #
    # Start UI loop
    #
    # ui.run()
