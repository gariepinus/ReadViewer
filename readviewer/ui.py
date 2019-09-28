import urwid


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

    def __init__(self, body, header, footer):
        global loop

        body = urwid.Filler(body, valign="top")

        header = urwid.AttrMap(urwid.Text(header, align="right"), "reversed")

        footer = urwid.Text(footer)
        super().__init__(body, header=header, footer=footer)
        loop.widget = self

    def keypress(self, size, key):
        if key == "Q":
            raise urwid.ExitMainLoop()
        else:
            return super().keypress(size, key)


class Main_Screen(Screen):

    def __init__(self):
        body = urwid.Pile([urwid.Text("Foo"), urwid.Text("Bar")])
        header = "Main_Header"
        footer = "Main_Footer"
        super().__init__(body, header, footer)

    def keypress(self, size, key):
        if key == "q":
            raise urwid.ExitMainLoop()
        if key in ["s", "S"]:
            Sessions_Screen()
        else:
            return super().keypress(size, key)


class Sessions_Screen(Screen):

    def __init__(self):
        body = urwid.Text("Foobar")
        header = "Session_Header"
        footer = "Session_Footer"
        super().__init__(body, header, footer)

    def keypress(self, size, key):
        if key == "q":
            Main_Screen()
        else:
            return super().keypress(size, key)
