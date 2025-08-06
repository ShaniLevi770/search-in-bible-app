from flask import Flask, request, render_template
import json

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

                results.append({
                    "book": verse["book"],
                    "chapter": verse["chapter"],
                    "verse": verse["verse"],
                    "text": original_text,
                    "highlighted": highlighted,
                })

    return results

def find_verse_by_name(name, verses):
    if not name:
        return None

    first_letter = name[0]
    last_letter = name[-1]

    for verse in verses:
        text = verse["text"].strip()
        if not text:
            continue

        cleaned_text = "".join(ch for ch in text if ch.isalnum())
        if cleaned_text and cleaned_text[0] == first_letter and cleaned_text[-1] == last_letter:
            return {
                "book": verse["book"],
                "chapter": verse["chapter"],
                "verse": verse["verse"],
                "text": verse["text"]
            }

    return None

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    name_result = None
    name_not_found = False
    search_word = ""
    skip = 0

    if request.method == "POST":
        search_word = request.form.get("word", "").strip()
        name = request.form.get("name", "").strip()

        if search_word:
            try:
                skip = int(request.form.get("skip", "0"))
            except ValueError:
                skip = 0
            results = skip_letter_search(search_word, skip, verses)

        if name:
            name_result = find_verse_by_name(name, verses)
            if name_result is None:
                name_not_found = True

    return render_template("index.html", results=results, word=search_word, skip=skip,
                           name_result=name_result, name_not_found=name_not_found)

if __name__ == "__main__":
    print("🚀 Flask app is starting...")
    app.run(debug=True)

