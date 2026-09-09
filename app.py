from flask import Flask, render_template, abort, request
import json
from pathlib import Path

app = Flask(__name__)

DATA_FILE = Path("data/processed/indicators.json")

def load_indicators():
    if not DATA_FILE.exists():
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

@app.route("/")
def dashboard():

    indicators = load_indicators()

    # Calculate statistics BEFORE filtering
    total = len(indicators)

    high = sum(
        1
        for item in indicators
        if item.get("analysis", {}).get("severity")
        == "high"
    )

    medium = sum(
        1
        for item in indicators
        if item.get("analysis", {}).get("severity")
        == "medium"
    )

    low = sum(
        1
        for item in indicators
        if item.get("analysis", {}).get("severity")
        == "low"
    )

    # Apply filter only to table data
    severity = request.args.get(
        "severity",
        ""
    ).lower()

    filtered_indicators = indicators

    if severity:

        filtered_indicators = [
            item
            for item in indicators
            if item.get("analysis", {}).get("severity")
            == severity
        ]

    return render_template(
        "dashboard.html",
        indicators=filtered_indicators,
        total=total,
        high=high,
        medium=medium,
        low=low,
        severity=severity
    )

@app.route("/indicator/<path:value>")
def indicator(value):

    indicators = load_indicators()

    for item in indicators:

        if item["indicator"]["value"] == value:

            return render_template(
                "indicator.html",
                indicator=item
            )

    abort(404)

if __name__ == "__main__":
    app.run(debug=True)