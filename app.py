from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

def add_weekdays(start_date, num_days):
    """Adds a given number of weekdays (Mon-Fri) to a start date."""
    current_date = start_date
    while num_days > 0:
        current_date += timedelta(days=1)
        if current_date.weekday() < 5:  # Monday to Friday (0-4)
            num_days -= 1
    return current_date

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.json
    start_date = datetime.strptime(data["start_date"], "%Y-%m-%d").date()
    total_days = data.get("total_days")
    weekdays = data.get("weekdays")
    history = data.get("history", [])

    # Ensure only one option is chosen
    if (total_days and weekdays) or (not total_days and not weekdays):
        return jsonify({"error": "Please enter either total days OR weekdays, not both!"}), 400

    if total_days:
        new_date = start_date + timedelta(days=int(total_days))
    elif weekdays:
        new_date = add_weekdays(start_date, int(weekdays))

    history.append(new_date.strftime("%Y-%m-%d"))  # Add new date to history

    return jsonify({
        "new_date": new_date.strftime("%Y-%m-%d"),
        "history": history
    })

if __name__ == "__main__":
    app.run(debug=True)
