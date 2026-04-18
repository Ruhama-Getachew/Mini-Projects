from flask import Flask, render_template, request
from logic import get_day_name

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        calendar = request.form["calendar"]
        date_input = request.form["date"].split("/")

        if len(date_input) != 3:
            result = "❌ Invalid format! Use dd/mm/yyyy"
        else:
            try:
                day = int(date_input[0])
                month = int(date_input[1])
                year = int(date_input[2])

                result = get_day_name(day, month, year, calendar)

            except ValueError:
                result = "❌ Please enter numbers only"

    return render_template("index.html", result=result)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

    