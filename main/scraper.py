import os
import re
import json
import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta

URL = "https://marthoma.in/prayer/"

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

# Sort keys longest-first so e.g. "1Corinthians" is tried before "1Co"
_BOOK_KEYS_SORTED = sorted(BOOKS_ML.keys(), key=len, reverse=True)

# Matches things like "Isa 52:7-15", "1Chr 29:10-18", "Heb 2", "Num 1-9"
REF_PATTERN = re.compile(
    r'\b((?:[1-3])?[A-Za-z]+)\s+(\d+(?:-\d+)?(?::\d+(?:-\d+)?)?)\b'
)


def get_next_sunday():
    today = date.today()
    days = (6 - today.weekday()) % 7
    if days == 0:
        days = 7
    return today + timedelta(days=days)


def to_malayalam(ref):
    if not ref:
        return ref
    for en in _BOOK_KEYS_SORTED:
        if ref.startswith(en):
            return ref.replace(en, BOOKS_ML[en], 1)
    return ref


def extract_refs(line):
    """Extract a list of scripture references like ['Isa 52:7-15', '2Tim 2:1-13']
    from a line that may contain one or more references separated by spaces."""
    if not line:
        return []
    return [f"{book} {chap}" for book, chap in REF_PATTERN.findall(line)]


def line_matches_date(lines, i, date_day, date_month_upper):
    """Handle both possible renderings of the date heading:
    - two separate lines: '05' then 'JUL' (case-insensitive)
    - one combined line: '05 JUL'
    """
    if i >= len(lines):
        return False, 0

    line = lines[i].strip()

    # Combined single line, e.g. "05 JUL"
    combined = re.match(r'^0*(\d{1,2})\s+([A-Za-z]{3,})$', line)
    if combined:
        day_part = combined.group(1).zfill(2)
        month_part = combined.group(2).upper()
        if day_part == date_day and month_part == date_month_upper:
            return True, 1

    # Two separate lines: day, then month
    if line == date_day or line.lstrip('0') == date_day.lstrip('0'):
        if i + 1 < len(lines) and lines[i + 1].strip().upper() == date_month_upper:
            return True, 2

    return False, 0


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
    date_day = sunday.strftime("%d")          
    date_month_upper = sunday.strftime("%b").upper()  

    print("Looking for:", date_day, date_month_upper)

    lines = [
        line.strip()
        for line in soup.get_text("\n").split("\n")
        if line.strip()
    ]

    print("First 300 lines:")
    for idx, line in enumerate(lines[:1000]):
        print(idx, repr(line))

    lesson1 = ""
    lesson2 = ""
    epistle = ""
    gospel = ""

    found = False

    def is_epistle_label(s):
        return s.replace(" ", "") in ("Epistle/Gospel", "EpistleGospel")

    def is_date_heading(s):
        return bool(re.match(r'^0*\d{1,2}\s+[A-Za-z]{3,}$', s))

    def collect_refs(lines, start, end, needed=2):
        """Collect references starting at `start`, walking forward line by
        line (references may be split across multiple lines, or combined
        onto one line) until `needed` refs are found or a new section
        boundary / date heading is hit."""
        refs = []
        k = start
        while k < end:
            line_k = lines[k]
            if (line_k == "Lessons" or is_epistle_label(line_k)
                    or line_k == "Evening Reading" or is_date_heading(line_k)
                    or line_k.startswith("Lectionary for")):
                break
            refs.extend(extract_refs(line_k))
            if len(refs) >= needed:
                break
            k += 1
        return refs

    for i in range(len(lines) - 1):
        matched, _consumed = line_matches_date(lines, i, date_day, date_month_upper)
        if not matched:
            continue

        print("Found date at line", i, "->", repr(lines[i]))
        found = True

        # Scan forward for the Lessons / Epistle-Gospel blocks, stopping once
        # we hit the next date entry or a new month section.
        window_end = min(i + 40, len(lines))
        for j in range(i, window_end):
            line_j = lines[j]

            # Stop if we've wandered into the next day's entry
            if j > i and is_date_heading(line_j):
                break
            if line_j.startswith("Lectionary for"):
                break

            if line_j == "Lessons":
                refs = collect_refs(lines, j + 1, window_end, needed=2)
                if len(refs) >= 1:
                    lesson1 = refs[0]
                if len(refs) >= 2:
                    lesson2 = refs[1]

            elif is_epistle_label(line_j):
                refs = collect_refs(lines, j + 1, window_end, needed=2)
                if len(refs) >= 1:
                    epistle = refs[0]
                if len(refs) >= 2:
                    gospel = refs[1]
                break  # nothing else we need comes after Epistle/Gospel

        break

    if not found:
        print("WARNING: No matching date entry found on the page for",
              date_day, date_month_upper)

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

        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Saved to {JSON_PATH}")

        data_ml = {
            "date": data["date"],
            "lesson1": to_malayalam(data["lesson1"]),
            "lesson2": to_malayalam(data["lesson2"]),
            "epistle": to_malayalam(data["epistle"]),
            "gospel": to_malayalam(data["gospel"]),
        }

        with open(ML_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(data_ml, f, indent=4, ensure_ascii=False)
        print(f"Saved to {ML_JSON_PATH}")

    except Exception as e:
        print("ERROR:", e)
        raise


if __name__ == "__main__":
    save_readings()
