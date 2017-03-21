"""
Project : ADE-ESIEE
File : test.py
Author : DELEVACQ Wallerand
Date : 21/03/2017
"""

from calendar_api import ADECalendar
from aurion_api import Aurion
from aurion_api import PersoException
from flask import Flask, request
import json

app = Flask(__name__)


@app.route("/api/ade-esiee/", methods=['POST'])
def get_calendar():
    username = request.form['username']
    password = request.form['password']
    month = request.form['month']
    day = request.form['day']

    if len(username) <= 0 or len(password) <= 0:
        return json.dumps("[{\"error\": \"empty password\"}]")

    aurion = Aurion()
    ade = ADECalendar()

    try:

        aurion.connect(username, password)
        myCours = aurion.get_unites_and_groups()
        ade.set_groups_unites(myCours)
        result = ade.get_cours_of(day, month)

        value = json.dumps(result)
        return value

    except PersoException as e:
        return json.dumps("[{\"error\": \""+str(e)+"\"}]")


if __name__ == "__main__":
    app.run()
