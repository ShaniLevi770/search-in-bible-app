from book_names import book_names
import json

with open("data/tanakh_hebrew.json", encoding="utf-8") as f:
    data = json.load(f)

books_seen = set()

for verse in data["verses"]:
    book_id = verse["book"]
    if book_id >= 5 and book_id not in books_seen:
        books_seen.add(book_id)
        book_name = book_names.get(book_id, "❌ חסר במפה")
        chapter = verse["chapter"]
        verse_num = verse["verse"]
        text = verse["text"]
        reversed_words = " ".join(word[::-1] for word in text.split())
        print(f"{book_id:2d}: {book_name}\n  פרק {chapter}, פסוק {verse_num}: {reversed_words}\n")
