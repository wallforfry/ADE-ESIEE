"""
Project : ADE-ESIEE
File : test.py
Author : DELEVACQ Wallerand
Date : 21/03/2017
"""

from calendar_api import ADECalendar
from aurion_api import Aurion
from aurion_api import PersoException
from flask import Flask, request, render_template
import json

flaskPort = 5000

app = Flask(__name__)


@app.route("/api/ade-esiee/groups", methods=['GET', 'POST'])
def get_groups():
    if request.method == 'GET':
        return render_template("index.html")

    username = request.form['username']
    password = request.form['password']

    if len(username) <= 0 or len(password) <= 0:
        return "[{\"error\": \"Wrong credentials\"}]"

    aurion = Aurion()

    try:

        aurion.connect(username, password)
        myCours = aurion.get_unites_and_groups()
        realNames = aurion.get_marks()

        result = []
        for cours in myCours:
            for name in realNames:
                if name.get("unite") in cours:
                    result.append({"unite": cours, "name": name.get("name")})

        value = json.dumps(result)
        return value

    except PersoException as e:
        return "[{\"error\": \"" + str(e) + "\"}]"


@app.route("/api/ade-esiee/agenda", methods=['GET', 'POST'])
def get_agenda():
    if request.method == 'GET':
        return render_template("index.html")

    groups = request.form['groups']
    mycours = [group.get("unite") for group in json.loads(groups)]

    ade = ADECalendar()

    try:
        ade.set_groups_unites(mycours)

        result = ade.get_all_cours()
        value = json.dumps(result)
        return value

    except PersoException as e:
        return "[{\"error\": \"" + str(e) + "\"}]"


@app.route("/api/ade-esiee/calendar", methods=['GET', 'POST'])
def get_calendar():
    if request.method == 'GET':
        return render_template("index.html")

    username = request.form['username']
    password = request.form['password']
    month = request.form['month']
    day = request.form['day']

    if len(username) <= 0 or len(password) <= 0:
        return "[{\"error\": \"Wrong credentials\"}]"

    aurion = Aurion()
    ade = ADECalendar()

    try:

        aurion.connect(username, password)
        myCours = aurion.get_unites_and_groups()
        ade.set_groups_unites(myCours)

        result = ade.get_all_cours()
        if len(month) > 0:
            result = ade.get_cours_by_month(result, month)
            if len(day) > 0:
                result = ade.get_cours_of(day, month)

        value = json.dumps(result)
        return value

    except PersoException as e:
        return "[{\"error\": \"" + str(e) + "\"}]"


@app.route("/api/ade-esiee/marks", methods=['GET', 'POST'])
def get_marks():
    if request.method == 'GET':
        return render_template("index.html")

    username = request.form['username']
    password = request.form['password']

    if len(username) <= 0 or len(password) <= 0:
        return "[{\"error\": \"Wrong credentials\"}]"

    aurion = Aurion()

    try:

        aurion.connect(username, password)
        marks = aurion.get_marks()
        value = json.dumps(marks)

        return value

    except PersoException as e:
        return "[{\"error\": \"" + str(e) + "\"}]"


@app.route("/api/ade-esiee/absences", methods=['GET', 'POST'])
def get_absences():
    if request.method == 'GET':
        return render_template("index.html")

    username = request.form['username']
    password = request.form['password']

    if len(username) <= 0 or len(password) <= 0:
        return "[{\"error\": \"Wrong credentials\"}]"

    aurion = Aurion()

    try:

        aurion.connect(username, password)
        absences = aurion.get_absences()
        value = json.dumps(absences)

        return value

    except PersoException as e:
        return "[{\"error\": \"" + str(e) + "\"}]"


@app.route("/api/ade-esiee/appreciations", methods=['GET', 'POST'])
def get_appreciations():
    if request.method == 'GET':
        return render_template("index.html")

    username = request.form['username']
    password = request.form['password']

    if len(username) <= 0 or len(password) <= 0:
        return "[{\"error\": \"Wrong credentials\"}]"

    aurion = Aurion()

    try:

        aurion.connect(username, password)
        appreciations = aurion.get_appreciations()
        value = json.dumps(appreciations)

        return value

    except PersoException as e:
        return "[{\"error\": \"" + str(e) + "\"}]"


if __name__ == "__main__":
    #ade = ADECalendar()
    #ade.set_groups_unites(["16_E4FR_RE4R23_2R"])
    #result = ade.get_all_cours()
    #print(result)
    app.run(host='0.0.0.0', port=flaskPort)

    # row = {"description":"\n1R\n2R\nTE3R21\nAURION\nNADAL F.\n(Exported :21/03/2017 23:00)"}
    # prof_finder(row)
