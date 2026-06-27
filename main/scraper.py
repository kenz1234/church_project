import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta
import re

URL = "https://marthoma.in/lectionary/"


def get_next_sunday():
    today = date.today()

    days = (6 - today.weekday()) % 7
    if days == 0:
        days = 7

    return today + timedelta(days=days)


def scrape_lectionary():

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(URL, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Convert page into clean text lines
    lines = [
        x.strip()
        for x in soup.get_text("\n").split("\n")
        if x.strip()
    ]

    sunday = get_next_sunday()

    day = str(sunday.day)
    month = sunday.strftime("%b")

    for i in range(len(lines)-1):

        # Because date is split into TWO lines:
        # 28
        # Jun
        if lines[i] == day and lines[i+1] == month:

            lesson1 = ""
            lesson2 = ""
            epistle = ""

            j = i

            while j < min(i + 30, len(lines)):

                if lines[j] == "Lessons":

                    lesson1 = lines[j+1]
                    lesson2 = lines[j+2]

                if lines[j] == "Epistle Gospel":

                    epistle = lines[j+1]
                    gospel = lines[j + 2]    

                    return {
                        "lesson1": lesson1,
                        "lesson2": lesson2,
                        "epistle": epistle,
                        "gospel": gospel,
                    }

                j += 1

    return None