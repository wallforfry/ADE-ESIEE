"""
Project : ADE-ESIEE
File : main.py
Author : DELEVACQ Wallerand
Date : 21/03/2017
"""
import planif_parser
from ade_api import ADEApi
from calendar_api import ADECalendar
from aurion_api import Aurion
from aurion_api import PersoException
from flask import Flask, request, render_template
import json
import unites_api

import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

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

        value = json.dumps(myCours)
        response = app.response_class(
            response=value,
            status=200,
            mimetype='application/json'
        )
        return response

    except PersoException as e:
        return "[{\"error\": \"" + str(e) + "\"}]"


@app.route("/api/ade-esiee/agenda/<mail>", methods=['GET', 'POST'])
def get_agenda_mail(mail):

    #ade = ADECalendar()
    ade = ADEApi()

    try:
        aurion = Aurion()
        unites_and_groups = aurion.get_unites_and_groups_from_csv(mail)
        ade.set_groups_unites(unites_and_groups)

        result = ade.get_all_cours()

        del ade
        if not result:
            return "[{\"error\": \"No events\"}]"

        value = json.dumps(result)
        response = app.response_class(
            response=value,
            status=200,
            mimetype='application/json'
        )
        return response

    except PersoException as e:
        return "[{\"error\": \"" + str(e) + "\"}]"


@app.route("/api/ade-esiee/agenda", methods=['GET', 'POST'])
def get_agenda():
    if request.method == 'GET':
        return render_template("index.html")

    mail = request.form['mail']
    #ade = ADECalendar()
    ade = ADEApi()

    try:
        aurion = Aurion()
        unites_and_groups = aurion.get_unites_and_groups_from_csv(mail)
        ade.set_groups_unites(unites_and_groups)

        result = ade.get_all_cours()

        del ade
        if not result:
            return "[{\"error\": \"No events\"}]"

        value = json.dumps(result)
        response = app.response_class(
            response=value,
            status=200,
            mimetype='application/json'
        )
        return response

    except PersoException as e:
        return "[{\"error\": \"" + str(e) + "\"}]"


@app.route("/api/ade-esiee/agendaFromGroups", methods=['GET', 'POST'])
def get_agenda_from_groups():
    if request.method == 'GET':
        return render_template("index.html")

    groups = request.form['groups']
    unites_and_groups = json.loads(groups)
    ade = ADECalendar()
    try:
        ade.set_groups_unites(unites_and_groups)
        result = ade.get_all_cours()
        if not result:
            return "[{\"error\": \"No events\"}]"
        value = json.dumps(result)
        response = app.response_class(
            response=value,
            status=200,
            mimetype='application/json'
        )
        return response

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
        response = app.response_class(
            response=value,
            status=200,
            mimetype='application/json'
        )
        return response

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

        response = app.response_class(
            response=value,
            status=200,
            mimetype='application/json'
        )
        return response

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

        response = app.response_class(
            response=value,
            status=200,
            mimetype='application/json'
        )
        return response

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

        response = app.response_class(
            response=value,
            status=200,
            mimetype='application/json'
        )
        return response

    except PersoException as e:
        return "[{\"error\": \"" + str(e) + "\"}]"


def update_ade_ics_file():
    planif_parser.download_ics_from_planif()


if __name__ == "__main__":
    # ade = ADECalendar()
    # ade.set_groups_unites(["16_E4FR_RE4R23_2R"])
    # result = ade.get_all_cours()
    # print(result)

    """update_ade_ics_file()

    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func=update_ade_ics_file,
        trigger=IntervalTrigger(minutes=10),
        id='printing_job',
        name='Print date and time every five seconds',
        replace_existing=True)
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
    """

    ade = ADEApi()
    ade.update_events()

    # Update events every 10 minutes
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func=ADEApi().update_events,
        trigger=IntervalTrigger(minutes=30),
        id='printing_job',
        name='Print date and time every five seconds',
        replace_existing=True)
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())

    # Update CSV file on api launch
    result = unites_api.get_row_on_website()
    unites_api.generate_csv_file(result)
    app.run(host='0.0.0.0', port=flaskPort)

    # row = {"description":"\n1R\n2R\nTE3R21\nAURION\nNADAL F.\n(Exported :21/03/2017 23:00)"}
    # prof_finder(row)
