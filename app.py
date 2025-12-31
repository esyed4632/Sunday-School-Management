from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Level lists
level_1 = []
level_2 = []
level_3 = []
level_4 = []
level_5 = []
level_6 = []
level_7 = []
level_8 = []
level_9 = []

def assign_level(age, name):
    if age == 5: level_1.append(name); return "Level 1"
    if age == 6: level_2.append(name); return "Level 2"
    if age == 7: level_3.append(name); return "Level 3"
    if age == 8: level_4.append(name); return "Level 4"
    if age == 9: level_5.append(name); return "Level 5"
    if age == 10: level_6.append(name); return "Level 6"
    if age == 11: level_7.append(name); return "Level 7"
    if age == 12: level_8.append(name); return "Level 8"
    if age == 13: level_9.append(name); return "Level 9"
    return None

@app.route("/")
def index():
    return render_template("register.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    child = data["Children"][0]
    name = child["Name"]
    age = int(child["Age"])

    if age < 5:
        return jsonify({"message":"Too Young — cannot apply"}), 400
    if age > 13:
        return jsonify({"message":"Too Old — too late"}), 400

    level = assign_level(age, name)
    return jsonify({"message":"Registration successful","level": level})

@app.route("/view")
def view_levels():
    return render_template("view.html", levels={
        "Level 1": level_1,
        "Level 2": level_2,
        "Level 3": level_3,
        "Level 4": level_4,
        "Level 5": level_5,
        "Level 6": level_6,
        "Level 7": level_7,
        "Level 8": level_8,
        "Level 9": level_9
    })

if __name__ == "__main__":
    app.run(debug=True)
