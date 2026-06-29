import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta
import json

URL = "https://marthoma.in/lectionary/"
JSON_PATH = "readings.json"


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

    response = requests.get(URL, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    sunday = get_next_sunday()

    date1 = sunday.strftime("%d %b")      # 05 Jul
    date2 = f"{sunday.day} {sunday.strftime('%b')}"   # 5 Jul

    lines = [
        x.strip()
        for x in soup.get_text("\n").split("\n")
        if x.strip()
    ]

    for i, line in enumerate(lines):
        if line in (date1, date2):

            lesson1 = lesson2 = epistle = gospel = ""

            for j in range(i, min(i + 20, len(lines))):

                if lines[j] == "Lessons":
                    lesson1 = lines[j + 1]
                    lesson2 = lines[j + 2]

                elif lines[j] == "Epistle Gospel":
                    epistle = lines[j + 1]
                    gospel = lines[j + 2]

                    return {
                        "date": sunday.strftime("%Y-%m-%d"),
                        "lesson1": lesson1,
                        "lesson2": lesson2,
                        "epistle": epistle,
                        "gospel": gospel,
                    }

    return {
        "date": sunday.strftime("%Y-%m-%d"),
        "lesson1": "",
        "lesson2": "",
        "epistle": "",
        "gospel": "",
    }

def save_readings():
    data = scrape_lectionary()
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"✅ Done! readings.json updated")
    print(json.dumps(data, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    save_readings()
