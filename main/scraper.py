import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta

URL = "https://marthoma.in/lectionary/"

BASE_DIR = os.path.dirname(__file__)
JSON_PATH = os.path.join(BASE_DIR, "readings.json")
ML_JSON_PATH = os.path.join(BASE_DIR, "readings_ml.json")

BOOKS_ML = {
    "Genesis": "ഉല്പത്തി",
    "Exodus": "പുറപ്പാട്",
    "Leviticus": "ലേവ്യർ",
    "Numbers": "സംഖ്യാപുസ്തകം",
    "Deuteronomy": "ആവർത്തനം",
    "Joshua": "യോശുവ",
    "Judges": "ന്യായാധിപന്മാർ",
    "Ruth": "രൂത്ത്",
    "1Chr": "1 ദിനവൃത്താന്തം",
    "2Chr": "2 ദിനവൃത്താന്തം",
    "1Tim": "1 തിമോത്തി",
    "2Tim": "2 തിമോത്തി",
    "1Cor": "1 കൊരിന്ത്യർ",
    "2Cor": "2 കൊരിന്ത്യർ",
    "Luke": "ലൂക്കാ",
    "John": "യോഹന്നാൻ",
    "Matt": "മത്തായി",
    "Mark": "മർക്കോസ്",
    "Acts": "അപ്പൊസ്തലപ്രവൃത്തികൾ",
    "Rom": "റോമർ",
    "Rev": "വെളിപ്പാട്"
}


def get_next_sunday():
    today = date.today()
    days = (6 - today.weekday()) % 7
    if days == 0:
        days = 7
    return today + timedelta(days=days)


def to_malayalam(ref):
    for en, ml in BOOKS_ML.items():
        if ref.startswith(en):
            return ref.replace(en, ml, 1)
    return ref


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

    # Save HTML for debugging
    DEBUG_PATH = os.path.join(BASE_DIR, "debug.html")
    with open(DEBUG_PATH, "w", encoding="utf-8") as f:
        f.write(response.text)

    print(f"Debug HTML saved to: {DEBUG_PATH}")

    soup = BeautifulSoup(response.text, "lxml")

    sunday = get_next_sunday()

    date_day = sunday.strftime("%d")      # 05
    date_month = sunday.strftime("%b")    # Jul

    print("Looking for:", date_day, date_month)

    lines = [
        line.strip()
        for line in soup.get_text("\n").split("\n")
        if line.strip()
    ]

    print("First 300 lines:")
    for idx, line in enumerate(lines[:300]):
        print(idx, repr(line))

    lesson1 = ""
    lesson2 = ""
    epistle = ""
    gospel = ""

    for i in range(len(lines) - 1):

        # Website stores the date as:
        # 05
        # Jul
        if lines[i] == date_day and lines[i + 1] == date_month:

            print("Found date!")

            for j in range(i, min(i + 30, len(lines))):

                if lines[j] == "Lessons" and j + 2 < len(lines):
                    lesson1 = lines[j + 1]
                    lesson2 = lines[j + 2]

                elif lines[j] == "Epistle Gospel" and j + 2 < len(lines):
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

    print(json.dumps(data, indent=4, ensure_ascii=False))

    return data


def save_readings():
    print("=== NEW SCRAPER VERSION ===")
    try:
        data = scrape_lectionary()

        # Save English JSON
        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"Saved to {JSON_PATH}")

        # Create Malayalam JSON
        data_ml = {
            "date": data["date"],
            "lesson1": to_malayalam(data["lesson1"]),
            "lesson2": to_malayalam(data["lesson2"]),
            "epistle": to_malayalam(data["epistle"]),
            "gospel": to_malayalam(data["gospel"]),
        }

        # Save Malayalam JSON
        with open(ML_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(data_ml, f, indent=4, ensure_ascii=False)

        print(f"Saved to {ML_JSON_PATH}")

    except Exception as e:
        print("ERROR:", e)
        raise


if __name__ == "__main__":
    save_readings()
