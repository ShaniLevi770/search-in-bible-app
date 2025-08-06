from flask import Flask, request, render_template
import json
import re
from book_names import book_names
from hebrew_numerals import hebrew_numerals

app = Flask(__name__)

# Load Hebrew Bible data
with open("data/tanakh_hebrew.json", encoding="utf-8") as f:
    verses = json.load(f)["verses"]

# Check if all characters are Hebrew letters
def is_valid_hebrew(text):
    return re.fullmatch(r'[\u0590-\u05FF]{2,}', text) is not None

# Highlight matching letters in a verse
def highlight_match(text, match_letters):
    if not match_letters:
        return text
    pattern = f"({re.escape(match_letters[0])}).*({re.escape(match_letters[1])})"
    return re.sub(pattern, r'<b>\1</b>...\2<b>\2</b>', text)

@app.route("/", methods=["GET", "POST"])
def home():
    results = []
    word = ""
    skip = 0
    name = ""
    warning = None

    if request.method == "POST":
        word = request.form.get("word", "").strip()
        name = request.form.get("name", "").strip()
        try:
            skip = int(request.form.get("skip", 0))
        except ValueError:
            skip = 0

        if name and not is_valid_hebrew(name):
            warning = "❗ השם חייב להכיל לפחות שתי אותיות בעברית בלבד."
        else:
            # Name-based search (first and last letter match)
            if name and len(name) >= 2:
                first, last = name[0], name[-1]
                for verse in verses:
                    clean_text = re.sub(r"[^\u0590-\u05FF]", "", verse["text"])
                    if clean_text and clean_text[0] == first and clean_text[-1] == last:
                        highlighted = verse["text"].replace(first, f"<b>{first}</b>", 1)
                        highlighted = highlighted[::-1].replace(last[::-1], f"<b>{last}</b>", 1)[::-1]
                        results.append({
                            "text": highlighted,
                            "source": f'{book_names.get(verse["book"], verse["book"])} '
                                      f'פרק {hebrew_numerals.get(str(verse["chapter"]), verse["chapter"])}, '
                                      f'פסוק {hebrew_numerals.get(str(verse["verse"]), verse["verse"])}'
                        })

            # Skip-letter search
            elif word and skip > 0:
                word = word.strip()
                for verse in verses:
                    clean = re.sub(r"[^\u0590-\u05FF]", "", verse["text"])
                    for i in range(len(clean) - skip * (len(word) - 1)):
                        letters = ''.join([clean[i + j * skip] for j in range(len(word))])
                        if letters == word:
                            highlighted = verse["text"]
                            for char in word:
                                highlighted = highlighted.replace(char, f"<b>{char}</b>", 1)
                            results.append({
                                "text": highlighted,
                                "source": f'{book_names.get(verse["book"], verse["book"])} '
                                          f'פרק {hebrew_numerals.get(str(verse["chapter"]), verse["chapter"])}, '
                                          f'פסוק {hebrew_numerals.get(str(verse["verse"]), verse["verse"])}'
                            })

    return render_template("index.html", results=results, word=word, skip=skip, name=name, warning=warning)

if __name__ == "__main__":
    app.run(debug=True)
