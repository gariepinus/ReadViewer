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
    parser.add_argument('-v', '--verbose', action='store_const',
                        const=True, default=False)
    return parser.parse_args()


CONSOLE_ARGUMENTS = _parse_arguments()
