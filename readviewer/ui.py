import urwid
from readviewer import version


loop = None


def run():
    """Load main screen and start ui loop."""
    global loop

    palette = [("reversed", "standout", ""),
               ("green", "light green", ""),
               ("dim", "dark gray", ""),
               ("bar0", "", ""),
               ("bar1", "", "dark blue"),
               ("bar2", "", "light blue")]

    loop = urwid.MainLoop(None, palette=palette)
    Main_Screen()
    loop.run()


class Screen(urwid.Frame):

    def __init__(self, body, keymap, book=None):
        global loop
        self.book = book

        body = urwid.Filler(body, valign="top")

        if book:
            header_text = "{} // ReadViewer v{}".format(book.title, version)
        else:
            header_text = "ReadViewer v{}".format(version)

        header = urwid.AttrMap(urwid.Text(header_text, align="right"), "reversed")
        footer = urwid.AttrMap(urwid.Text(str(Keymap(["Q::Quit", "q::Back/Quit"] + keymap))), "dim")

        super().__init__(body, header=header, footer=footer)
        loop.widget = self

    def keypress(self, size, key):
        if key == "Q":
            raise urwid.ExitMainLoop()
        else:
            return super().keypress(size, key)


class Main_Screen(Screen):

    def __init__(self, book=None):
        body = urwid.Pile([urwid.Text("Foo"), urwid.Text("Bar")])

        keymap = ["s::Sessions"]
        
        super().__init__(body, keymap, book)

    def keypress(self, size, key):
        if key == "q" and self.book is None:
            raise urwid.ExitMainLoop()
        elif key == "q":
            Main_Screen
        if key in ["s", "S"]:
            Sessions_Screen()
        else:
            return super().keypress(size, key)


class Sessions_Screen(Screen):

    def __init__(self, book=None):
        body = urwid.Text("Foobar")
        footer = "Session_Footer"
        super().__init__(body, footer, book)

    def keypress(self, size, key):
        if key == "q":
            Main_Screen(self.book)
        else:
            return super().keypress(size, key)


class Keymap():

    def __init__(self, lst):
        self.lst = lst

    def __str__(self):
        r = ""
        for key in self.lst:
            r += "{}  ".format(key)
        return r