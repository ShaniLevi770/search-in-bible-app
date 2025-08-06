import json

with open("data/tanakh_hebrew.json", encoding="utf-8") as f:
    data = json.load(f)

print("Top-level keys:", list(data.keys())[:5])  # first few books or keys
print("Sample content:", json.dumps(data, ensure_ascii=False, indent=2)[:1000])  # show part of the structure
