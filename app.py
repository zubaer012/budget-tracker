from flask import Flask, render_template, request, redirect, url_for, jsonify
import csv
import os

app = Flask(__name__)
DATA_PATH = "data/budget.csv"
os.makedirs("data", exist_ok=True)

def load_data():
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, newline="") as f:
        reader = csv.DictReader(f)
        return [{"amount": float(r["amount"]), "category": r["category"], "type": r["type"]} for r in reader]

def save_data(entries):
    with open(DATA_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["amount", "category", "type"])
        writer.writeheader()
        writer.writerows(entries)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        amount = float(request.form["amount"])
        category = request.form["category"]
        type_ = request.form["type"]
        entries = load_data()
        entries.append({"amount": amount, "category": category, "type": type_})
        save_data(entries)
        return redirect(url_for("index"))

    entries = load_data()
    balance = sum(e["amount"] if e["type"] == "Income" else -e["amount"] for e in entries)
    return render_template("index.html", entries=entries, balance=balance)

@app.route("/chart-data")
def chart_data():
    from collections import defaultdict
    data = defaultdict(float)
    for e in load_data():
        if e["type"] == "Expense":
            data[e["category"]] += e["amount"]
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
