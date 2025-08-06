book_names = {
    1: "בראשית",
    2: "שמות",
    3: "ויקרא",
    4: "במדבר",
    5: "דברים",
    6: "יהושע",
    7: "שופטים",
    8: "רות",
    9: "שמואל א׳",
    10: "שמואל ב׳",
    11: "מלכים א׳",
    12: "מלכים ב׳",
    13: "דברי הימים א׳",
    14: "דברי הימים ב׳",
    15: "עזרא",
    16: "נחמיה",
    17: "אסתר",
    18: "איוב",
    19: "תהילים",
    20: "משלי",
    21: "קהלת",
    22: "שיר השירים",
    23: "ישעיהו",
    24: "ירמיהו",
    25: "איכה",
    26: "יחזקאל",
    27: "דניאל",
    28: "הושע",
    29: "יואל",
    30: "עמוס",
    31: "עובדיה",
    32: "יונה",
    33: "מיכה",
    34: "נחום",
    35: "חבקוק",
    36: "צפניה",
    37: "חגי",
    38: "זכריה",
    39: "מלאכי"
}

import json

with open("data/tanakh_hebrew.json", encoding="utf-8") as f:
    data = json.load(f)

books_seen = set()

for verse in data["verses"]:
    book_id = verse["book"]
    if book_id >= 12 and book_id not in books_seen:
        books_seen.add(book_id)
        book_name = book_names.get(book_id, "❌ חסר במפה")
        chapter = verse["chapter"]
        verse_num = verse["verse"]
        text = verse["text"]
        reversed_words = " ".join(word[::-1] for word in text.split())
        print(f"{book_id:2d}: {book_name}\n  פרק {chapter}, פסוק {verse_num}: {reversed_words}\n")
