from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    print("📡 בקשה הגיעה לשרת")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
