import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta

URL = "https://marthoma.in/lectionary/"

BASE_DIR = os.path.dirname(__file__)
JSON_PATH = os.path.join(BASE_DIR, "readings.json")


def get_next_sunday():
    today = date.today()
    days = (6 - today.weekday()) % 7
    if days == 0:
        days = 7
    return today + timedelta(days=days)


def scrape_lectionary():
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/137.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(URL, headers=headers, timeout=30)
    response.raise_for_status()

    print("Status Code:", response.status_code)
    print("Final URL:", response.url)
    print("Downloaded:", len(response.text), "characters")

    DEBUG_PATH = os.path.join(BASE_DIR, "debug.html")

    with open(DEBUG_PATH, "w", encoding="utf-8") as f:
        f.write(response.text)

    print(f"Debug HTML saved to: {DEBUG_PATH}")

    soup = BeautifulSoup(response.text, "lxml")

    sunday = get_next_sunday()

    date_padded = sunday.strftime("%d %b")
    date_plain = f"{sunday.day} {sunday.strftime('%b')}"

    print("Looking for:", date_padded, "or", date_plain)

    lines = [
        line.strip()
        for line in soup.get_text("\n").split("\n")
        if line.strip()
    ]

    lesson1 = lesson2 = epistle = gospel = ""

    for i, line in enumerate(lines):

        if line == date_padded or line == date_plain:

            print("Found date!")

            for j in range(i, min(i + 20, len(lines))):

                if lines[j] == "Lessons":
                    if j + 2 < len(lines):
                        lesson1 = lines[j + 1]
                        lesson2 = lines[j + 2]

                elif lines[j] == "Epistle Gospel":
                    if j + 2 < len(lines):
                        epistle = lines[j + 1]
                        gospel = lines[j + 2]
                        break

            break

    data = {
        "date": sunday.strftime("%Y-%m-%d"),
        "lesson1": lesson1,
        "lesson2": lesson2,
        "epistle": epistle,
        "gospel": gospel,
    }

    print(json.dumps(data, indent=4))

    return data


def save_readings():
    try:
        data = scrape_lectionary()

        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"Saved to {JSON_PATH}")

    except Exception as e:
        print("ERROR:", e)
        raise


if __name__ == "__main__":
    save_readings()
