import urwid
from readviewer import version
import readviewer.data as data
import os


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
    Main_Screen().draw()
    loop.run()


def book_chosen(button, choice):
    Main_Screen(choice).draw()


class Screen(urwid.Frame):

    def __init__(self, content, path=[], keymap=[]):
        self.content = content
        self.path = path
        self.keymap = keymap

    def draw(self):
        super().__init__(self.content, header=self.header, footer=self.footer)
        global loop
        loop.widget = self

    def keypress(self, size, key):
        if key == "Q":
            raise urwid.ExitMainLoop()
        else:
            return super().keypress(size, key)

    @property
    def body(self):
        return urwid.Filler(self.content, valign="top")

    @property
    def header(self):
        header_text = "/ReadViewer v{}".format(version)
        for level in self.path:
            header_text = "{}/{}".format(level, header_text)
        return urwid.AttrMap(urwid.Text(header_text, align="right"), "reversed")

    @property
    def footer(self):
        keylist = "\nQ::Quit  q::Back/Quit"
        for key in self.keymap:
            keylist += "  {}".format(key)
        return urwid.AttrMap(urwid.Text(keylist), "dim")


class Main_Screen(Screen):

    def __init__(self, book=None, focus=None):
        self.book = book
        body = urwid.Pile([self.stat_box, self.graph, self.scroll_list])
        keymap = ["s::Sessions"]
        if book:
            path = [book.title[:40]]
        else:
            path = []
        super().__init__(body, path, keymap)

    def keypress(self, size, key):
        if key == "q" and self.book is None:
            raise urwid.ExitMainLoop()
        elif key == "q":
            Main_Screen().draw()
        if key == "s":
            Sessions_Screen(self.book).draw()
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
                speed=self.book.speed, 
                score=self.book.average_score)
        else:
            stats = "{pages} pages in {time} over {sessions} sessions since {timestamp}.\n[Average speed: {speed} pages/hour; Average score: {score}]".format(
                pages=data.cumulate("pages"), 
                time=data.cumulate("duration"), 
                sessions=len(data.sessions), 
                timestamp=data.sessions[0].timestamp.date(), 
                speed=data.average("speed"), 
                score=data.average("score"))

        box = urwid.LineBox(urwid.Text(stats))
        return ("pack", box)

    @property
    def graph(self):
        if self.book:
            sessions = self.book.sessions[-100:]
        else:
            sessions = data.sessions[-100:]
        graph = Bar_graph([session.score for session in sessions], x="Sessions [most recent {}]".format(len(sessions)), y="Score")
        return (20, graph)

    @property
    def scroll_list(self):
        rows, columns = os.popen('stty size', 'r').read().split()
        height = int(int(rows) - 30)

        if self.book:
            return (height, Session_List(self.book.sessions))
        else:
            body = [urwid.Divider(), urwid.AttrMap(urwid.Text("Currently reading"), "dim"), urwid.Divider()]

            for book in data.unfinished_books():
                button = urwid.Button("{}\n{}".format(book, book.stats), on_press=book_chosen, user_data=book)
                body.append(urwid.AttrMap(button, None, focus_map='green'))

            body.append(urwid.Divider())
            body.append(urwid.AttrMap(urwid.Text("Finished"), "dim"))
            body.append(urwid.Divider())

            for book in data.finished_books():
                button = urwid.Button("{}\n{}".format(book, book.stats), on_press=book_chosen, user_data=book)
                body.append(urwid.AttrMap(button, None, focus_map='green'))

            lst = urwid.ListBox(urwid.SimpleFocusListWalker(body))
            padding = urwid.Padding(lst, left=1, right=1)
            return (height, padding)


class Sessions_Screen(Screen):

    def __init__(self, book=None):
        self.book = book
        keymap = ["S::Sort"]
        path = []
        if book:
            path.append(book.title[:40])
            sessions = book.sessions
        else:
            sessions = data.sessions
        path.append("Sessions")

        rows, columns = os.popen('stty size', 'r').read().split()
        height = int(int(rows) - 8)
        super().__init__(urwid.Pile([urwid.Divider() ,(height, Session_List(sessions))]), path, keymap)

    def keypress(self, size, key):
        if key == "q":
            Main_Screen(self.book).draw()
        else:
            return super().keypress(size, key)


class Bar_graph(urwid.Overlay):

    def __init__(self, values, heading=None, x=None, y=None):
        self.values = values

        widgets = []
        if heading:
            widgets.append(("pack", urwid.AttrMap(urwid.Text(" == {} ==".format(heading)), "heading")))
        
        if x and y:
            legend = " x ↦ {}  /  y ↥ {} [0-{}]".format(x,y,max(self.values))
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

class Session_List(urwid.Padding):

    def __init__(self, sessions):
    
        body = [urwid.Divider()]

        for session in sessions:
            button = urwid.Text("{}".format(session))
            body.append(urwid.AttrMap(button, None))

        lst = urwid.ListBox(urwid.SimpleFocusListWalker(body))
        walker = urwid.ListBox(urwid.SimpleFocusListWalker(body))
        padding = urwid.Padding(walker, left=1, right=1)
        super().__init__(walker, left=1, right=1)
