from flask import Flask, request, render_template
import json
import re
from book_names import book_names
from hebrew_numerals import hebrew_numerals

app = Flask(__name__)

# Load Hebrew Bible data
with open("data/tanakh_hebrew.json", encoding="utf-8") as f:
    verses = json.load(f)["verses"]

def get_verse_reference(verse):
    book = book_names.get(str(verse["book"]), f"ספר {verse['book']}")
    chapter = hebrew_numerals.get(str(verse["chapter"]), verse["chapter"])
    verse_num = hebrew_numerals.get(str(verse["verse"]), verse["verse"])
    return f"{book} - פרק {chapter}, פסוק {verse_num}"

@app.route("/", methods=["GET", "POST"])
def index():
    matches = []
    name = ""
    warning = ""

    if request.method == "POST":
        name = request.form["name"].strip()

        if not re.fullmatch(r"[א-ת]{2,}", name):
            warning = "❗ אנא הזן שם בעברית (לפחות שתי אותיות)"
        else:
            first_letter = name[0]
            last_letter = name[-1]

            for v in verses:
                text = v["text"].strip()
                if text and text[0] == first_letter and text[-1] == last_letter:
                    highlighted = (
                        f"<b>{text[0]}</b>{text[1:-1]}<b>{text[-1]}</b>"
                        if len(text) > 1 else f"<b>{text}</b>"
                    )
                    matches.append({
                        "source": get_verse_reference(v),
                        "highlighted": highlighted
                    })

    return render_template("index.html", results=matches, name=name, warning=warning)

if __name__ == "__main__":
    app.run(debug=True)
