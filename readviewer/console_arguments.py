import argparse


def _parse_arguments():
    parser = argparse.ArgumentParser(description="""Visualize
                         ReadTracker data in your terminal.""",
                                     epilog="""ReadTracker by Christoffer
                         Klang: https://github.com/christoffer/readtracker""",
                                     prog="readviewer")
    parser.add_argument('file', metavar='FILE', type=str,
                        help="""the exported
                         JSON file you want to view""")
    return parser.parse_args()


CONSOLE_ARGUMENTS = _parse_arguments()
