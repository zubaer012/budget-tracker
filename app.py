from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
from datetime import datetime
import csv
import json
import os

app = Flask(__name__)

DATA_PATH = "data/budget.csv"
LIMITS_PATH = "data/limits.json"
os.makedirs("data", exist_ok=True)

CATEGORIES = [
    "General", "Food", "Rent", "Travel", "Entertainment",
    "Utilities", "Healthcare", "Education", "Savings", "Gifts"
]

def load_data():
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, newline="") as f:
        reader = csv.DictReader(f)
        return [
            {
                "amount": float(r["amount"]),
                "category": r["category"],
                "type": r["type"],
                "date": r.get("date", "")
            }
            for r in reader
        ]

def save_data(entries):
    with open(DATA_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["amount", "category", "type", "date"])
        writer.writeheader()
        writer.writerows(entries)

def load_limits():
    if not os.path.exists(LIMITS_PATH):
        return {}
    with open(LIMITS_PATH) as f:
        return json.load(f)

def save_limits(limits):
    with open(LIMITS_PATH, "w") as f:
        json.dump(limits, f)

def calculate_warnings(entries, limits):
    from collections import defaultdict
    spent = defaultdict(float)
    for e in entries:
        if e["type"] == "Expense":
            spent[e["category"]] += e["amount"]

    warnings = []
    for cat, limit in limits.items():
        if spent[cat] > limit:
            over = spent[cat] - limit
            warnings.append(f"⚠️ Over budget in '{cat}' by ${over:.2f}")
    return warnings

def calculate_monthly_stats(entries):
    income = sum(e["amount"] for e in entries if e["type"] == "Income")
    expenses = sum(e["amount"] for e in entries if e["type"] == "Expense")
    return {
        "income": income,
        "expenses": expenses,
        "savings": income - expenses
    }

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        amount = float(request.form["amount"])
        category = request.form["category"]
        type_ = request.form["type"]
        entries = load_data()
        entries.append({
            "amount": amount,
            "category": category,
            "type": type_,
            "date": datetime.now().strftime("%Y-%m-%d")
        })
        save_data(entries)
        return redirect(url_for("index"))

    selected_month = request.args.get("month") or datetime.now().strftime("%Y-%m")
    all_entries = load_data()
    entries = [e for e in all_entries if e["date"].startswith(selected_month)]
    balance = sum(e["amount"] if e["type"] == "Income" else -e["amount"] for e in entries)
    limits = load_limits()
    warnings = calculate_warnings(entries, limits)
    monthly_stats = calculate_monthly_stats(entries)

    return render_template(
        "index.html",
        entries=entries,
        balance=balance,
        warnings=warnings,
        limits=limits,
        categories=CATEGORIES,
        selected_month=selected_month,
        monthly_stats=monthly_stats
    )

@app.route("/delete-entry", methods=["POST"])
def delete_entry():
    try:
        entries = load_data()
        index = int(request.form["entry_index"])
        entries.pop(index)
        save_data(entries)
        return redirect(url_for("index"))
    except (ValueError, IndexError):
        return redirect(url_for("index"))

@app.route("/export-csv")
def export_csv():
    from io import StringIO
    import csv
    
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Date", "Category", "Type", "Amount"])
    
    entries = load_data()
    for entry in entries:
        writer.writerow([
            entry["date"],
            entry["category"],
            entry["type"],
            entry["amount"]
        ])
    
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=budget_data.csv"}
    )

@app.route("/reset", methods=["POST"])
def reset():
    try:
        # Clear budget.csv
        with open(DATA_PATH, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["amount", "category", "type", "date"])
            writer.writeheader()
        
        # Clear limits.json
        with open(LIMITS_PATH, "w") as f:
            json.dump({}, f)
            
        return redirect(url_for("index"))
    except Exception as e:
        print(f"Error during reset: {e}")
        return redirect(url_for("index"))

@app.route("/set-limit", methods=["POST"])
def set_limit():
    category = request.form["limit_category"]
    try:
        limit = float(request.form["limit_amount"])
    except ValueError:
        return redirect(url_for("index"))
    limits = load_limits()
    limits[category] = limit
    save_limits(limits)
    return redirect(url_for("index"))

@app.route("/chart-data")
def chart_data():
    from collections import defaultdict
    month = request.args.get("month") or datetime.now().strftime("%Y-%m")
    filtered = [e for e in load_data() if e["date"].startswith(month)]
    data = defaultdict(float)
    for e in filtered:
        if e["type"] == "Expense":
            data[e["category"]] += e["amount"]
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
