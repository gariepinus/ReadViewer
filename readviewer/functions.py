from statistics import mean
import readviewer.data as data

def calculate_scores():
    """Calculate every sessions score."""

    max_duration = max([session.duration for session in data.sessions])
    max_pages = max([session.pages for session in data.sessions])

    one_percent_duration = max_duration / 100
    one_percent_pages = max_pages / 100

    for session in data.sessions:
        duration_score = session.duration / one_percent_duration
        pages_score = session.pages / one_percent_pages

        session.set_score(int(mean([duration_score, pages_score])))
