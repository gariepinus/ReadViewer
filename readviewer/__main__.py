import sys
import readviewer.data as data
#import readviewer.ui as ui

if __name__ == "__main__":

    #
    # Eval cli arguments
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

    #
    # Load json data
    #
    data.load(file_path)

    #
    # Start UI loop
    #
    #ui.run()
