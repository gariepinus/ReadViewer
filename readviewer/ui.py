import urwid
from readviewer import version
import readviewer.data as data


loop = None


def run():
    """Load main screen and start ui loop."""
    global loop

    palette = [("reversed", "standout", ""),
               ("green", "light green", ""),
               ("dim", "dark gray", ""),
               ("heading", "white, bold", ""),
               ("bar0", "dark blue", ""),
               ("bar1", "", "dark cyan"),
               ("bar2", "", "light cyan")]

    loop = urwid.MainLoop(None, palette=palette)
    Main_Screen()
    loop.run()


class Screen(urwid.Frame):

    def __init__(self, body, keymap=[], book=None):
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
        self.book = book
        body = urwid.Pile([self.stat_box, self.graph, urwid.Text("Foo"), urwid.Text("Bar")])

        keymap = ["s::Sessions"]

        super().__init__(body, keymap, book)


    def keypress(self, size, key):
        if key == "q" and self.book is None:
            raise urwid.ExitMainLoop()
        elif key == "q":
            Main_Screen
        if key == "s":
            Sessions_Screen(self.book)
        else:
            return super().keypress(size, key)

    @property
    def stat_box(self):
        if self.book:
            stats = "{pages} pages ({progress}%) in {time} over {sessions} sessions since {timestamp}.\n[Average speed: {speed} pages/hour; Average score: {score}]".format(
                pages=self.book.current_page,
                progress=self.book.progress,
                time=self.book.duration, 
                sessions=len(self.book.sessions), 
                timestamp=self.book.sessions[0].timestamp.date(), 
                speed=data.average("speed"), 
                score=data.average("score"))
        else:
            stats = "{pages} pages in {time} over {sessions} sessions since {timestamp}.\n[Average speed: {speed} pages/hour; Average score: {score}]".format(
                pages=data.cumulate("pages"), 
                time=data.cumulate("duration"), 
                sessions=len(data.sessions), 
                timestamp=data.sessions[0].timestamp.date(), 
                speed=data.average("speed"), 
                score=data.average("score"))

        return urwid.LineBox(urwid.Text(stats))

    @property
    def graph(self):
        return (20, Bar_graph([session.score for session in data.sessions], "Score", "Sessions", "Score"))

class Sessions_Screen(Screen):

    def __init__(self, book=None):
        body = urwid.Text("Foobar")
        super().__init__(body, [], book)

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


class Bar_graph(urwid.Overlay):

    def __init__(self, values, heading=None, x=None, y=None):
        self.values = values

        widgets = []
        if heading:
            widgets.append(("pack", urwid.AttrMap(urwid.Text("  == {} ==".format(heading)), "heading")))
        
        if x and y:
            legend = "  x ↦ {}  /  y ↥ {} [0-{}]".format(x,y,max(self.values))
            widgets.append(("pack", urwid.AttrMap(urwid.Text(legend), "dim")))

        widgets.append(("pack", urwid.Divider()))
        widgets.append(self.graph)

        top_w = urwid.Pile(widgets)
        bottom_w = urwid.AttrWrap(urwid.SolidFill("\N{MEDIUM SHADE}"), "bar0")
        super().__init__(top_w, bottom_w, "center", ("relative", 98), "middle", 18)

    @property
    def graph(self):
        graph = urwid.BarGraph(["bar0", "bar1", "bar2"])

        lst = []
        i = True
        for value in self.values:
            if i:
                lst.append([value,0])
                i = False
            else:
                lst.append([0,value])
                i = True

        graph.set_data(lst, max(self.values))
        return graph
