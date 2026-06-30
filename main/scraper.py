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

    # Pentateuch
    "Genesis": "ഉല്പത്തി",
    "Gen": "ഉല്പത്തി",

    "Exodus": "പുറപ്പാട്",
    "Exod": "പുറപ്പാട്",

    "Leviticus": "ലേവ്യപുസ്തകം",
    "Lev": "ലേവ്യപുസ്തകം",

    "Numbers": "സംഖ്യാപുസ്തകം",
    "Num": "സംഖ്യാപുസ്തകം",

    "Deuteronomy": "ആവർത്തനം",
    "Deut": "ആവർത്തനം",

    # Historical Books
    "Joshua": "യോശുവ",
    "Josh": "യോശുവ",

    "Judges": "ന്യായാധിപന്മാർ",
    "Judg": "ന്യായാധിപന്മാർ",

    "Ruth": "രൂത്ത്",

    "1Samuel": "1 ശമൂവേൽ",
    "1 Samuel": "1 ശമൂവേൽ",
    "1Sam": "1 ശമൂവേൽ",

    "2Samuel": "2 ശമൂവേൽ",
    "2 Samuel": "2 ശമൂവേൽ",
    "2Sam": "2 ശമൂവേൽ",

    "1Kings": "1 രാജാക്കന്മാർ",
    "1 Kings": "1 രാജാക്കന്മാർ",
    "1Kgs": "1 രാജാക്കന്മാർ",

    "2Kings": "2 രാജാക്കന്മാർ",
    "2 Kings": "2 രാജാക്കന്മാർ",
    "2Kgs": "2 രാജാക്കന്മാർ",

    "1Chronicles": "1 ദിനവൃത്താന്തം",
    "1 Chronicles": "1 ദിനവൃത്താന്തം",
    "1Chr": "1 ദിനവൃത്താന്തം",

    "2Chronicles": "2 ദിനവൃത്താന്തം",
    "2 Chronicles": "2 ദിനവൃത്താന്തം",
    "2Chr": "2 ദിനവൃത്താന്തം",

    "Ezra": "എസ്രാ",
    "Neh": "നെഹെമ്യാവു",
    "Nehemiah": "നെഹെമ്യാവു",

    "Esth": "എസ്ഥേർ",
    "Esther": "എസ്ഥേർ",

    # Wisdom Books
    "Job": "ഇയ്യോബ്",

    "Psalm": "സങ്കീർത്തനങ്ങൾ",
    "Psalms": "സങ്കീർത്തനങ്ങൾ",
    "Ps": "സങ്കീർത്തനങ്ങൾ",

    "Prov": "സദൃശ്യവാക്യങ്ങൾ",
    "Proverbs": "സദൃശ്യവാക്യങ്ങൾ",

    "Eccl": "സഭാപ്രസംഗി",
    "Ecclesiastes": "സഭാപ്രസംഗി",

    "Song": "ഉത്തമഗീതം",
    "Song of Solomon": "ഉത്തമഗീതം",

    # Major Prophets
    "Isaiah": "യെശയ്യാവ്",
    "Isa": "യെശയ്യാവ്",

    "Jeremiah": "യിരെമ്യാവ്",
    "Jer": "യിരെമ്യാവ്",

    "Lamentations": "വിലാപങ്ങൾ",
    "Lam": "വിലാപങ്ങൾ",

    "Ezekiel": "യെഹെസ്കേൽ",
    "Ezek": "യെഹെസ്കേൽ",

    "Daniel": "ദാനിയേൽ",
    "Dan": "ദാനിയേൽ",

    # Minor Prophets
    "Hosea": "ഹോശേയ",
    "Hos": "ഹോശേയ",

    "Joel": "യോവേൽ",

    "Amos": "ആമോസ്",

    "Obadiah": "ഓബദ്യാവു",
    "Obad": "ഓബദ്യാവു",

    "Jonah": "യോനാ",

    "Micah": "മീഖാ",
    "Mic": "മീഖാ",

    "Nahum": "നഹൂം",
    "Nah": "നഹൂം",

    "Habakkuk": "ഹബക്കൂക്ക്",
    "Hab": "ഹബക്കൂക്ക്",

    "Zephaniah": "സെഫന്യാവു",
    "Zeph": "സെഫന്യാവു",

    "Haggai": "ഹഗ്ഗായി",
    "Hag": "ഹഗ്ഗായി",

    "Zechariah": "സെഖര്യാവു",
    "Zech": "സെഖര്യാവു",

    "Malachi": "മലാഖി",
    "Mal": "മലാഖി",

    # Gospels
    "Matthew": "മത്തായി",
    "Matt": "മത്തായി",
    "Mt": "മത്തായി",

    "Mark": "മർക്കോസ്",
    "Mk": "മർക്കോസ്",

    "Luke": "ലൂക്കോസ്",
    "Lk": "ലൂക്കോസ്",

    "John": "യോഹന്നാൻ",
    "Jn": "യോഹന്നാൻ",

    # Acts
    "Acts": "അപ്പൊസ്തലപ്രവൃത്തികൾ",

    # Pauline Epistles
    "Romans": "റോമർ",
    "Rom": "റോമർ",

    "1Corinthians": "1 കൊരിന്ത്യർ",
    "1 Corinthians": "1 കൊരിന്ത്യർ",
    "1Cor": "1 കൊരിന്ത്യർ",

    "2Corinthians": "2 കൊരിന്ത്യർ",
    "2 Corinthians": "2 കൊരിന്ത്യർ",
    "2Cor": "2 കൊരിന്ത്യർ",

    "Galatians": "ഗലാത്യർ",
    "Gal": "ഗലാത്യർ",

    "Ephesians": "എഫേസ്യർ",
    "Eph": "എഫേസ്യർ",

    "Philippians": "ഫിലിപ്പിയർ",
    "Phil": "ഫിലിപ്പിയർ",

    "Colossians": "കൊലൊസ്സ്യർ",
    "Col": "കൊലൊസ്സ്യർ",

    "1Thessalonians": "1 തെസ്സലൊനിക്ക്യർ",
    "1 Thessalonians": "1 തെസ്സലൊനിക്ക്യർ",
    "1Thess": "1 തെസ്സലൊനിക്ക്യർ",

    "2Thessalonians": "2 തെസ്സലൊനിക്ക്യർ",
    "2 Thessalonians": "2 തെസ്സലൊനിക്ക്യർ",
    "2Thess": "2 തെസ്സലൊനിക്ക്യർ",

    "1Timothy": "1 തിമൊഥെയൊസ്",
    "1 Timothy": "1 തിമൊഥെയൊസ്",
    "1Tim": "1 തിമൊഥെയൊസ്",

    "2Timothy": "2 തിമൊഥെയൊസ്",
    "2 Timothy": "2 തിമൊഥെയൊസ്",
    "2Tim": "2 തിമൊഥെയൊസ്",

    "Titus": "തീത്തൊസ്",
    "Tit": "തീത്തൊസ്",

    "Philemon": "ഫിലേമോൻ",
    "Phlm": "ഫിലേമോൻ",

    # General Epistles
    "Hebrews": "എബ്രായർ",
    "Heb": "എബ്രായർ",

    "James": "യാക്കോബ്",
    "Jas": "യാക്കോബ്",

    "1Peter": "1 പത്രോസ്",
    "1 Peter": "1 പത്രോസ്",
    "1Pet": "1 പത്രോസ്",

    "2Peter": "2 പത്രോസ്",
    "2 Peter": "2 പത്രോസ്",
    "2Pet": "2 പത്രോസ്",

    "1John": "1 യോഹന്നാൻ",
    "1 John": "1 യോഹന്നാൻ",

    "2John": "2 യോഹന്നാൻ",
    "2 John": "2 യോഹന്നാൻ",

    "3John": "3 യോഹന്നാൻ",
    "3 John": "3 യോഹന്നാൻ",

    "Jude": "യൂദാ",

    # Revelation
    "Revelation": "വെളിപ്പാട്",
    "Rev": "വെളിപ്പാട്",

    "Ge": "ഉല്പത്തി",
    "Gn": "ഉല്പത്തി",

    "Ex": "പുറപ്പാട്",

    "Le": "ലേവ്യപുസ്തകം",

    "Nu": "സംഖ്യാപുസ്തകം",
    "Nm": "സംഖ്യാപുസ്തകം",

    "Dt": "ആവർത്തനം",

    "Jos": "യോശുവ",

    "Jdg": "ന്യായാധിപന്മാർ",
    "Jgs": "ന്യായാധിപന്മാർ",

    "Ru": "രൂത്ത്",

    "1Sa": "1 ശമൂവേൽ",
    "2Sa": "2 ശമൂവേൽ",

    "1Ki": "1 രാജാക്കന്മാർ",
    "2Ki": "2 രാജാക്കന്മാർ",

    "1Ch": "1 ദിനവൃത്താന്തം",
    "2Ch": "2 ദിനവൃത്താന്തം",

    "Ezr": "എസ്രാ",

    "Ne": "നെഹെമ്യാവു",

    "Es": "എസ്ഥേർ",

    "Pr": "സദൃശ്യവാക്യങ്ങൾ",

    "Ecc": "സഭാപ്രസംഗി",

    "So": "ഉത്തമഗീതം",
    "Song": "ഉത്തമഗീതം",
    "SOS": "ഉത്തമഗീതം",

    "Is": "യെശയ്യാവ്",

    "Je": "യിരെമ്യാവ്",

    "La": "വിലാപങ്ങൾ",

    "Eze": "യെഹെസ്കേൽ",
    "Ezk": "യെഹെസ്കേൽ",

    "Da": "ദാനിയേൽ",

    "Ho": "ഹോശേയ",

    "Joe": "യോവേൽ",

    "Am": "ആമോസ്",

    "Ob": "ഓബദ്യാവു",

    "Jon": "യോനാ",

    "Mic": "മീഖാ",

    "Na": "നഹൂം",

    "Hb": "ഹബക്കൂക്ക്",

    "Zep": "സെഫന്യാവു",

    "Hg": "ഹഗ്ഗായി",

    "Zec": "സെഖര്യാവു",

    "Ml": "മലാഖി",


    "Mat": "മത്തായി",

    "Mrk": "മർക്കോസ്",
    "Mr": "മർക്കോസ്",

    "Lu": "ലൂക്കോസ്",
    "Luk": "ലൂക്കോസ്",

    "Joh": "യോഹന്നാൻ",
    "Jhn": "യോഹന്നാൻ",

    "Ac": "അപ്പൊസ്തലപ്രവൃത്തികൾ",

    "Ro": "റോമർ",

    "1Co": "1 കൊരിന്ത്യർ",
    "2Co": "2 കൊരിന്ത്യർ",

    "Ga": "ഗലാത്യർ",

    "Ep": "എഫേസ്യർ",

    "Php": "ഫിലിപ്പിയർ",
    "Phip": "ഫിലിപ്പിയർ",

    "Co": "കൊലൊസ്സ്യർ",

    "1Th": "1 തെസ്സലൊനിക്ക്യർ",
    "2Th": "2 തെസ്സലൊനിക്ക്യർ",

    "1Ti": "1 തിമൊഥെയൊസ്",
    "2Ti": "2 തിമൊഥെയൊസ്",

    "Ti": "തീത്തൊസ്",

    "Phm": "ഫിലേമോൻ",

    "He": "എബ്രായർ",

    "Jam": "യാക്കോബ്",

    "1Pe": "1 പത്രോസ്",
    "2Pe": "2 പത്രോസ്",

    "1Jn": "1 യോഹന്നാൻ",
    "2Jn": "2 യോഹന്നാൻ",
    "3Jn": "3 യോഹന്നാൻ",

    "Jud": "യൂദാ",

    "Re": "വെളിപ്പാട്",


    
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
