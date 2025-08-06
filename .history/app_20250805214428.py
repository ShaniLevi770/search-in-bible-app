from flask import Flask, request, render_template
import json
from book_names import book_names
from hebrew_numerals import hebrew_numerals

app = Flask(__name__)

# Load Hebrew Bible data
with open("data/tanakh_hebrew.json", encoding="utf-8") as f:
    raw = json.load(f)
    verses = raw["verses"]


def is_bad_char(ch):
    return (
        ch == " " or
        ch in ("\u200E", "\u200F", "\u00A0") or  # direction markers and non-breaking space
        ('֐' <= ch <= 'ׇ')  # Hebrew vowel marks
    )


def find_verse_by_name(name, verses):
    if not name:
        return None

    first_letter = name[0]
    last_letter = name[-1]

    for verse in verses:
        text = verse["text"].strip()
        if not text:
            continue

        # הסרת תווים בעייתיים
        stripped = "".join(ch for ch in text if ch.isalnum() or ch == '׳' or ch == '״')
        if stripped and stripped[0] == first_letter and stripped[-1] == last_letter:
            return {
                "book": verse["book"],
                "chapter": verse["chapter"],
                "verse": verse["verse"],
                "text": verse["text"]
            }

    return None


def skip_letter_search(word, skip, verses):
    results = []
    word = word.replace(" ", "")
    word_length = len(word)

    for verse in verses:
        original_text = verse["text"]
        clean_text = ""
        map_index = []

        for idx, ch in enumerate(original_text):
            if not is_bad_char(ch):
                clean_text += ch
                map_index.append(idx)

        for start in range(len(clean_text) - (word_length - 1) * (skip + 1)):
            indices = [start + i * (skip + 1) for i in range(word_length)]
            candidate = "".join(clean_text[i] for i in indices)

            if candidate == word:
                highlight_indices = [map_index[i] for i in indices]
                highlighted = ""
                for i, ch in enumerate(original_text):
                    if i in highlight_indices:
                        highlighted += f"<b>{ch}</b>"
                    else:
                        highlighted += ch

                book = book_names.get(verse["book"], f"ספר {verse['book']}")
                chapter = hebrew_numerals.get(verse["chapter"], str(verse["chapter"]))
                verse_num = hebrew_numerals.get(verse["verse"], str(verse["verse"]))

                source = f"{book} פרק {chapter} פסוק {verse_num}"

                results.append({
                    "book": verse["book"],
                    "chapter": verse["chapter"],
                    "verse": verse["verse"],
                    "text": original_text,
                    "highlighted": highlighted,
                    "source": source
                })

    return results


@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    name_result = None
    name_not_found = False
    search_word = ""
    skip = 0

    if request.method == "POST":
        if "word" in request.form:
            search_word = request.form["word"].strip()
            skip_input = request.form["skip"].strip()

            try:
                skip = int(skip_input)
            except ValueError:
                skip = 0

            results = skip_letter_search(search_word, skip, verses)

        if "personal_name" in request.form:
            personal_name = request.form["personal_name"].strip()
            name_result = find_verse_by_name(personal_name, verses)
            if name_result is None:
                name_not_found = True

    return render_template(
        "index.html",
        results=results,
        word=search_word,
        skip=skip,
        name_result=name_result,
        name_not_found=name_not_found,
        book_names=book_names,
        hebrew_numerals=hebrew_numerals
    )




if __name__ == "__main__":
    print("🚀 Flask app is starting...")
    app.run(debug=True)
