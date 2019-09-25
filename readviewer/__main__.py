import sys
import readviewer.data as data

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

    data.load(file_path)