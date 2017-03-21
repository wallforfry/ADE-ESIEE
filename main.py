"""
Project : ADE-ESIEE
File : test.py
Author : DELEVACQ Wallerand
Date : 21/03/2017
"""

from calendar_api import ADECalendar
from aurion_api import Aurion
from aurion_api import PersoException

if __name__ == "__main__":
    print("Welcome")

    username = input("Username : ")
    password = input("Password : ")

    aurion = Aurion()
    ade = ADECalendar()

    try:

        aurion.connect(username, password)
        myCours = aurion.get_unites_and_groups()
        ade.set_groups_unites(myCours)
        result = ade.get_cours_of("21", "03")

        for elt in result:
            print(elt["name"])

    except PersoException as e:
        print(e)
