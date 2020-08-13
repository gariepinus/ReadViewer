import readviewer.database as database
from readviewer.console_arguments import CONSOLE_ARGUMENTS as args

if __name__ == "__main__":

    #
    # Load json data
    #
    database.load(args.file)
