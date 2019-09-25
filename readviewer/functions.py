from statistics import mean
from functools import reduce
from datetime import timedelta
import readviewer.data as data

def cumulate(stat, day=None,month=None,year=None):
    """Return the cumulative score, session number, pages, duration or average speed for one day month or year or all sessions."""

    if day is not None:
        lst = list(filter(lambda session: (str(session.timestamp.date()) == day), data.sessions))
    elif month is not None:
        lst = list(filter(lambda session: ("{}-{:0>2}".format(session.timestamp.year, session.timestamp.month) == month), data.sessions))
    elif year is not None:
        lst = list(filter(lambda session: (str(session.timestamp.year) == year), data.sessions))
    else:
        lst = data.sessions

    if stat == "score":
        return int(sum([session.score for session in lst]))
    elif stat == "sessions":
        return len(lst)
    elif stat == "pages":
        return sum([session.pages for session in lst])
    elif stat == "duration":
        return reduce(lambda a,b: a + b.duration, lst, timedelta())
    elif stat == "speed" and len(lst) > 0:
        return int(mean([session.speed for session in lst]))
    else:
        return 0
