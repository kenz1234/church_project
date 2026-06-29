import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta
import json
import os

URL = "https://marthoma.in/lectionary/"

# ✅ Fixed path - points exactly to your folder
JSON_PATH = "/home/kavungumprayarstthomasmarthoma/church_project_src/main/readings.json"

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
    lines = [
        x.strip()
        for x in soup.get_text("\n").split("\n")
        if x.strip()
    ]
    sunday = get_next_sunday()
    day = str(sunday.day)
    month = sunday.strftime("%b")

    for i in range(len(lines) - 1):
        if lines[i] == day and lines[i + 1] == month:
            lesson1 = ""
            lesson2 = ""
            epistle = ""
            gospel = ""
            j = i
            while j < min(i + 30, len(lines)):
                if lines[j] == "Lessons":
                    lesson1 = lines[j + 1]
                    lesson2 = lines[j + 2]
                if lines[j] == "Epistle Gospel":
                    epistle = lines[j + 1]
                    gospel = lines[j + 2]
                    return {
                        "date": sunday.strftime("%Y-%m-%d"),
                        "lesson1": lesson1,
                        "lesson2": lesson2,
                        "epistle": epistle,
                        "gospel": gospel,
                    }
                j += 1

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
    print(f"✅ Done! Saved to: {JSON_PATH}")
    print(f"Data: {json.dumps(data, indent=2)}")

if __name__ == "__main__":
    save_readings()
