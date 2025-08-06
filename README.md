# 🔍 Hebrew Bible Pattern Search App

This web application enables users to explore fascinating patterns in the Hebrew Bible (Tanakh) using skip-letter sequences (Equidistant Letter Sequences – ELS), as well as find verses that match a given name through initial and final letter matching based on Hebrew names.
It is designed for anyone curious about hidden structures and textual patterns in biblical Hebrew.

---

## ✨ Features

### 📘 1. Skip-Letter Search (ELS)
- Input a Hebrew word and a skip interval (0 = regular search, 1 = every other letter, etc.).
- The app scans the Hebrew Bible and identifies matching letter sequences.
- Highlights matching letters in the verse.
- Shows the verse source (book, chapter, and verse) in Hebrew.

### 📗 2. Name-Based Verse Finder
- Input a Hebrew name (at least 2 Hebrew letters).
- Finds all verses that **start and end** with the same letters as the name.
- Highlights the matching letters in the verse text.
- Displays accurate verse source in Hebrew.

### 💡 3. Dual Interface
- Two separate input forms:
  - Skip-letter word search
  - Name-based verse search
- Fully supports **Right-to-Left (RTL)** layout for Hebrew.
- Clean and responsive UI.



---

## 🛠️ Technology Stack

- **Backend:** Python 3, Flask
- **Frontend:** HTML, CSS (RTL layout)
- **Data Source:** `data/tanakh_hebrew.json` — the Hebrew Bible in structured JSON format

---

## 📦 Folder Structure
hebrew_rag_app/
│
├── app.py # Main Flask application
├── templates/
│ └── index.html # Frontend UI
├── data/
│ └── tanakh_hebrew.json # Hebrew Bible data
├── book_names.py # Hebrew book name mapping
├── hebrew_numerals.py # Hebrew numerals for chapter/verse
├── .gitignore
└── README.md



---

## 🚀 How to Run Locally

### 🔧 Prerequisites:
- Python 3.8+
- `pip`
- (Optional) virtual environment

### ✅ Setup Instructions

```bash
# 1. Clone the repository
git clone https://github.com/ShaniLevi770/search-in-bible-app.git
cd search-in-bible-app

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate      # On Windows
# source venv/bin/activate # On Mac/Linux

# 3. Install dependencies
pip install flask

# 4. Run the app
python app.py



📜 Example Searches
Skip-Letter Search:
Word: "אמת"

Skip: 3
→ Will find verses where the letters "א", "מ", and "ת" appear every 4th character.

Name-Based Search:
Name: "משה"
→ Will find verses that start with "מ" and end with "ה".

❗ Notes
Only Hebrew letters are supported.

For name search, input must be at least 2 characters.

Verses with invalid or empty text are ignored during processing.

📚 Credits
Hebrew Bible JSON: based on public biblical text resources.

Developed using Flask and pure Python.

Created with love ❤️📖

📄 License
This project is licensed under the MIT License — see LICENSE file for details.
