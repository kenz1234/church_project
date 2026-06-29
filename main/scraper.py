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
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    sunday = get_next_sunday()

    # Website format is like "05 Jul" or "5 Jul"
    # We try both zero-padded and non-padded
    date_str_padded = sunday.strftime("%d %b")       # "05 Jul"
    date_str_plain  = f"{sunday.day} {sunday.strftime('%b')}"  # "5 Jul"

    # Find all list items on the page
    for li in soup.find_all("li"):
        text = li.get_text(" ", strip=True)

        # Check if this list item starts with our date
        if text.startswith(date_str_padded) or text.startswith(date_str_plain):
            lesson1  = ""
            lesson2  = ""
            epistle  = ""
            gospel   = ""

            # Get all the text lines inside this block
            lines = [x.strip() for x in li.get_text("\n").split("\n") if x.strip()]

            for i, line in enumerate(lines):
                if line == "Lessons" and i + 2 < len(lines):
                    lesson1 = lines[i + 1]
                    lesson2 = lines[i + 2]
                if line == "Epistle Gospel" and i + 2 < len(lines):
                    epistle = lines[i + 1]
                    gospel  = lines[i + 2]

            return {
                "date":    sunday.strftime("%Y-%m-%d"),
                "lesson1": lesson1,
                "lesson2": lesson2,
                "epistle": epistle,
                "gospel":  gospel,
            }

    # Not found
    return {
        "date":    sunday.strftime("%Y-%m-%d"),
        "lesson1": "",
        "lesson2": "",
        "epistle": "",
        "gospel":  "",
    }

def save_readings():
    data = scrape_lectionary()
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"✅ Done! readings.json updated")
    print(json.dumps(data, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    save_readings()
