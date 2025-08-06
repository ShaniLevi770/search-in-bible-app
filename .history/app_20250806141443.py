from flask import Flask, request, render_template
import json
from book_names import book_names
from hebrew_numerals import hebrew_numerals

app = Flask(__name__)

# Load data
with open("data/tanakh_hebrew.json", encoding="utf-8") as f:
    verses = json.load(f)["verses"]

def is_bad_char(ch):
    return ch in (" ", "\u200E", "\u200F", "\u00A0") or ('֐' <= ch <= 'ׇ')

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
                highlighted = "".join(f"<b>{ch}</b>" if i in highlight_indices else ch for i, ch in enumerate(original_text))

                book = book_names.get(verse["book"], verse["book"])
                chapter = hebrew_numerals.get(verse["chapter"], verse["chapter"])
                verse_num = hebrew_numerals.get(verse["verse"], verse["verse"])
                source = f"{book} פרק {chapter} פסוק {verse_num}"

                results.append({
                    "highlighted": highlighted,
                    "source": source
                })

    return results

def find_verses_by_name(name, verses):
    results = []
    if not name:
        return results

    first_letter = name[0]
    last_letter = name[-1]

    for verse in verses:
        text = verse["text"].strip()
        if not text:
            continue

        clean = "".join(ch for ch in text if ch.isalnum() or ch in ['׳', '״'])
        if clean and clean[0] == first_letter and clean[-1] == last_letter:
            highlighted = f"<b>{text[0]}</b>{text[1:-2]}<b>{text[-2]}</b>"

            book = book_names.get(verse["book"], verse["book"])
            chapter = hebrew_numerals.get(verse["chapter"], verse["chapter"])
            verse_num = hebrew_numerals.get(verse["verse"], verse["verse"])
            source = f"{book} פרק {chapter} פסוק {verse_num}"

            results.append({
                "highlighted": highlighted,
                "source": source
            })

    return results

@app.route("/", methods=["GET", "POST"])
def index():
    word = ""
    skip = 0
    results = []
    name_results = []
    name_not_found = False

    if request.method == "POST":
        word = request.form.get("word", "").strip()
        skip_input = request.form.get("skip", "0").strip()
        try:
            skip = int(skip_input)
        except ValueError:
            skip = 0
        if word:
            results = skip_letter_search(word, skip, verses)

        name = request.form.get("name", "").strip()
        if name:
            if all('\u0590' <= ch <= '\u05EA' for ch in name) and len(name) > 1:
                name_results = find_verses_by_name(name, verses)
                if not name_results:
                    name_not_found = "❌ לא נמצאו פסוקים שמתחילים ומסתיימים באותיות המתאימות לשם"
            else:
                name_not_found = "❌ רק אותיות בעברית, שתי אותיות או יותר"



    return render_template("index.html", word=word, skip=skip,
                           results=results,
                           name_results=name_results,
                           name_not_found=name_not_found)

if __name__ == "__main__":
    app.run(debug=True)
