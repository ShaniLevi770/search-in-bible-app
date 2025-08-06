from flask import Flask, request, render_template
import json
import os

app = Flask(__name__)

# Load Bible text from JSON file (one time on app startup)
with open("hebrew_bible.json", encoding="utf-8") as f:
    verses = json.load(f)

def highlight_letters(text, letters):
    """Highlight all letters in a word (non-consecutive)."""
    for ch in set(letters):
        text = text.replace(ch, f"<b>{ch}</b>")
    return text

def search_by_skip(word, skip):
    """Find verses where word appears with skip (0 = normal search)."""
    results = []

    for book in verses:
        for chapter in verses[book]:
            for verse_num in verses[book][chapter]:
                text = verses[book][chapter][verse_num]
                clean_text = ''.join(c for c in text if c.isalpha())

                if skip == 0:
                    if word in clean_text:
                        highlighted = text.replace(word, f"<b>{word}</b>")
                        results.append({
                            "source": f"{book} פרק {chapter} פסוק {verse_num}",
                            "highlighted": highlighted
                        })
                else:
                    # Check skip-letter match
                    for i in range(len(clean_text) - (skip * (len(word)-1))):
                        letters = [clean_text[i + j*skip] for j in range(len(word))]
                        if ''.join(letters) == word:
                            highlighted = highlight_letters(text, word)
                            results.append({
                                "source": f"{book} פרק {chapter} פסוק {verse_num}",
                                "highlighted": highlighted
                            })
                            break  # Only first match per verse

    return results

def find_verses_by_name(name, data):
    """Find verses that start and end with letters like the name."""
    first_letter = name[0]
    last_letter = name[-1]
    results = []

    for book in data:
        for chapter in data[book]:
            for verse_num in data[book][chapter]:
                text = data[book][chapter][verse_num].strip()
                if not text:
                    continue

                text_letters = ''.join([c for c in text if c.isalpha()])
                if text_letters and text_letters[0] == first_letter and text_letters[-1] == last_letter:
                    highlighted = f"<b>{first_letter}</b>{text[1:-1]}<b>{last_letter}</b>" if len(text) > 2 else f"<b>{text}</b>"
                    results.append({
                        "source": f"{book} פרק {chapter} פסוק {verse_num}",
                        "highlighted": highlighted
                    })

    return results


@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    name_results = []
    name_not_found = False
    word = ""
    skip = 0
    name = ""

    if request.method == "POST":
        if "word" in request.form:
            word = request.form["word"].strip()
            skip = int(request.form.get("skip", 0))
            if word:
                results = search_by_skip(word, skip)

        if "name" in request.form:
            name = request.form["name"].strip()
            if len(name) >= 2 and all('\u0590' <= ch <= '\u05FF' for ch in name):
                name_results = find_verses_by_name(name, verses)
                if not name_results:
                    name_not_found = True

    return render_template("index.html",
                           results=results,
                           word=word,
                           skip=skip,
                           name=name,
                           name_results=name_results,
                           name_not_found=name_not_found)


if __name__ == "__main__":
    print("🚀 Flask app is running")
    app.run(debug=True)
