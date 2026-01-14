from flask import Flask, render_template, request, session, redirect, url_for, jsonify, Response
import datetime
import csv
import io

app = Flask(__name__)
app.secret_key = "supersecretkey"

# -----------------------------
# In-memory storage
# -----------------------------
levels = {
    "Level 1": [],
    "Level 2": [],
    "Level 3": [],
    "Level 4": [],
    "Level 5": [],
    "Level 6": [],
    "Level 7": []
}

attendance_records = {}  # For storing attendance by date, level, student

STAFF_USER = "admin"
STAFF_PASS = "password123"

# -----------------------------
# Staff login/logout
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form.get("username") == STAFF_USER and request.form.get("password") == STAFF_PASS:
            session["staff"] = True
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid username or password"
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# -----------------------------
# Staff dashboard
# -----------------------------
@app.route("/dashboard")
def dashboard():
    if not session.get("staff"):
        return redirect(url_for("login"))
    return render_template("dashboard.html", levels=levels)

# -----------------------------
# Attendance page
# -----------------------------
@app.route("/attendance")
def attendance():
    if not session.get("staff"):
        return redirect(url_for("login"))
    today = datetime.date.today().isoformat()
    return render_template("attendance.html", levels=levels, today=today)

# -----------------------------
# Save attendance
# -----------------------------
@app.route("/attendance/save", methods=["POST"])
def save_attendance():
    if not session.get("staff"):
        return jsonify({"error": "Unauthorized"}), 403
    data = request.get_json()
    date = data.get("date")
    level = data.get("level")
    records = data.get("records", {})

    if date not in attendance_records:
        attendance_records[date] = {}
    if level not in attendance_records[date]:
        attendance_records[date][level] = {}
    attendance_records[date][level].update(records)

    return jsonify({"status": "success"})

# -----------------------------
# Export attendance CSV
# -----------------------------
@app.route("/attendance/export")
def attendance_export():
    if not session.get("staff"):
        return redirect(url_for("login"))

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Date", "Level", "Student", "Status"])

    for date, levels_data in attendance_records.items():
        for level, students in levels_data.items():
            for student, status in students.items():
                writer.writerow([date, level, student, status])

    output.seek(0)
    return Response(output, mimetype="text/csv",
                    headers={"Content-Disposition":"attachment;filename=attendance.csv"})

# -----------------------------
# Run the app
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
