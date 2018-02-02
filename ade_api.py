"""
Project : ade-esiee
File : ade_api.py
Author : DELEVACQ Wallerand
Date : 02/02/18
"""
import atexit

import re
from datetime import datetime

import requests
from xml.etree import ElementTree

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from aurion_api import Aurion
from unites_api import search_unite_from_csv


class ADEApi():
    project_id = "7"
    base_url = "https://planif.esiee.fr/jsp/webapi"
    session_id = ""

    events = ()
    groups_and_unites = ()
    unites = ()
    groups = {}

    def __init__(self):
        self._get_events_from_xml()
        pass

    def update_events(self):
        self._connect()
        self._set_project_id()
        self._set_events_to_xml()
        self._disconnect()

    def _connect(self):
        url = self.base_url + "?function=connect&login=lecteur1&password="

        response = requests.get(url)

        tree = ElementTree.fromstring(response.text)

        self.session_id = tree.attrib["id"]

    def _disconnect(self):
        url = self.base_url + "?function=disconnect"

        response = requests.get(url)

        return response.status_code == 200

    def set_groups_unites(self, aurion_data):
        # self.groups_and_unites.append({"unite": "FLE-4102", "groupe": "E4inter"})
        self.groups_and_unites = tuple()
        self.unites = tuple()
        for data in aurion_data:
            groups = self.groups_finder(data)
            self.groups.update(dict([(self.format_unites(data), groups)]))
            for group in groups:
                d = dict([("unite", self.format_unites(data)), ("groupe", group)])
                self.groups_and_unites += tuple([d])
                self.unites += tuple([self.format_unites(data)])

    def _set_project_id(self):
        url = self.base_url + "?sessionId=" + self.session_id + "&function=setProject&projectId=" + self.project_id

        response = requests.get(url)

        return response.status_code == 200

    def _get_events_from_xml(self):
        try:
            tree = ElementTree.parse("ade.xml")
            self.events = tree.getroot().findall("event")
        except FileNotFoundError as e:
            print(e)
            self.update_events()

    def _set_events_to_xml(self):
        url = self.base_url + "?sessionId=" + self.session_id + "&function=getEvents&tree=true&detail=8"

        response = requests.get(url)

        with open("ade.xml", mode="w") as f:
            f.write(response.text)

    @staticmethod
    def groups_finder(data):
        '''

        :param data: row of aurion provided data
        :return: list of different possible cases of group number
        '''
        back = [m.start() for m in re.finditer("_", data[::-1])]
        if "EIG_2022" in data:
            real_group = data[len(data) - back[0]:]
            return [real_group, real_group[0].upper() + real_group[1:].lower(),
                    real_group[0].lower() + real_group[1:].upper(), real_group.upper(), real_group.lower()]
        if "EIG" in data:
            return data[len(data) - 3:len(data) - 2] + data[len(data) - 2:len(data) - 1].lower() + data[len(data):]

        if "PR_3001" in data and len(back) > 4:
            real_group = data[len(data) - back[0]:].replace("_", "-")
            return [real_group, real_group[0].upper() + real_group[1:].lower(),
                    real_group[0].lower() + real_group[1:].upper(), real_group.upper(), real_group.lower()]

        if "PR" in data and len(back) > 4:
            real_group = data[len(data) - back[1]:].replace("_", "-")
            return [real_group, real_group[0].upper() + real_group[1:].lower(),
                    real_group[0].lower() + real_group[1:].upper(), real_group.upper(), real_group.lower()]

        if "EN3" in data:
            real_group = data[len(data) - back[0]:].replace("_", "-")
            if len(real_group) >= 2:
                return [real_group, real_group[0].upper() + real_group[1:].lower(),
                        real_group[0].lower() + real_group[1:].upper(), real_group.upper(), real_group.lower()]
            else:
                return ["xx"]

        if len(back) <= 1:
            # return [data[data.find("_")+1:]]
            return ["", data[data.find("_") + 1:]]

        real_group = data[len(data) - back[0]:]
        if len(real_group) >= 2:
            return [real_group, real_group[0].upper() + real_group[1:].lower(),
                    real_group[0].lower() + real_group[1:].upper(), real_group.upper(), real_group.lower()]
        # elif not "EN3" in data:
        else:
            return [real_group, real_group.upper(), real_group.lower()]

    @staticmethod
    def format_unites(data):
        '''

        :param data: row of aurion provided data
        :return: unite name formatted likes unite name in calendar api
        '''
        back = [m.start() for m in re.finditer("_", data)]
        if len(back) == 1:
            real_group = data[back[0] + 1:]
            real_group = real_group.replace("_", "-")
            # Correction pour les noms de promos
            real_group += ":"
            return real_group
        if len(back) == 3:  # 16_E4FR_RE4R23_2R
            real_group = data[back[1] + 1:back[2]]
            real_group = real_group.replace("_", "-")
            return real_group
        if len(back) == 4:  # 16_E2_IGE_2102_2
            real_group = data[back[1] + 1:back[3]]
            real_group = real_group.replace("_", "-")
            return real_group
        if len(back) == 5:  # 16_E2_ESP_2003_S2_2
            if "PR" in data:
                real_group = data[back[1] + 1:back[3]]
                real_group = real_group.replace("_", "-")
            else:
                real_group = data[back[1] + 1:back[4]]
                real_group = real_group.replace("_", "-")
            return real_group

    @staticmethod
    def _has_cours(xml_event, unite, groups):
        if unite in xml_event.attrib["name"]:
            rows = (xml_event.find("resources")).findall("resource")
            for row in rows:
                if "trainee" in row.attrib["category"]:
                    if row.attrib["name"] in groups:
                        return True
        return False

    @staticmethod
    def _get_instructor(xml_event):
        instructors = []
        for row in (xml_event.find("resources")).findall("resource"):
            if "instructor" in row.attrib["category"]:
                instructors.append(row.attrib["name"])
        return instructors

    @staticmethod
    def _get_name(xml_event):
        for row in (xml_event.find("resources")).findall("resource"):
            if "category6" in row.attrib["category"]:
                return xml_event.attrib["name"]
        return ""

    @staticmethod
    def _get_unite(xml_event):
        for row in (xml_event.find("resources")).findall("resource"):
            if "category6" in row.attrib["category"]:
                return row.attrib["name"]
        return ""

    @staticmethod
    def _get_classroom(xml_event):
        classrooms = []
        for row in (xml_event.find("resources")).findall("resource"):
            if "classroom" in row.attrib["category"]:
                classrooms.append(row.attrib["name"])
        return classrooms

    @staticmethod
    def _get_start_date(xml_event):
        date = xml_event.attrib["date"]
        start_hour = xml_event.attrib["startHour"]
        start_hour = str(int(start_hour[:start_hour.find(":")]) - 1) + start_hour[start_hour.find(":"):]

        date = datetime.strptime(date, "%d/%m/%Y")
        return datetime.strftime(date, "%Y-%m-%d") + "T" + start_hour + ":00.000Z"

    @staticmethod
    def _get_end_date(xml_event):
        date = xml_event.attrib["date"]
        end_hour = xml_event.attrib["endHour"]
        end_hour = str(int(end_hour[:end_hour.find(":")]) + 1) + end_hour[end_hour.find(":"):]

        date = datetime.strptime(date, "%d/%m/%Y")
        return datetime.strftime(date, "%Y-%m-%d") + "T" + end_hour + ":00.000Z"

    def get_all_cours(self):
        result = []
        for event in self.events:
            unite = self._get_unite(event)
            if unite in self.unites:
                group = self.groups[unite]
                if self._has_cours(event, unite, group):
                    name = self._get_name(event)
                    instructors = self._get_instructor(event)
                    unite = self._get_unite(event)
                    classrooms = self._get_classroom(event)
                    start = self._get_start_date(event)
                    end = self._get_end_date(event)

                    obj = {"name": name, "prof": ", ".join(instructors), "rooms": ", ".join(classrooms),
                           "start": start, "end": end, "unite": search_unite_from_csv(unite),
                           "description": unite + " " + ", ".join(instructors)}
                    if obj not in result:
                        result.append(obj)

        return result



if __name__ == "__main__":
    aurion = Aurion()
    ade = ADEApi()

    groups = aurion.get_unites_and_groups_from_csv("hueta")
    ade.set_groups_unites(groups)

    print(ade.groups_and_unites)

    #print(type(ade.groups_and_unites))
    #print(type(ade.events[0]))
    print(ade.get_all_cours())
