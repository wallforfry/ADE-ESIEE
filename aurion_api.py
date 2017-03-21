"""
Project : ADE-ESIEE
File : test.py
Author : DELEVACQ Wallerand
Date : 21/03/2017
"""

from html.parser import HTMLParser
import requests


class DataParser(HTMLParser):
    """
    Parse data in aurion page
    """

    def __init__(self):
        super().__init__()
        self.recording = 0
        self.data = []

    def handle_starttag(self, tag, attrs):
        if tag != 'td':
            return
        if self.recording:
            self.recording += 1
            return
        self.recording = 1

    def handle_endtag(self, tag):
        if tag == 'td' and self.recording:
            self.recording -= 1

    def handle_data(self, data):
        if data.strip():
            if self.recording:
                self.data.append(data.strip())


class MenuParser(HTMLParser):
    """
    Parse menu idt value
    """

    def __init__(self):
        super().__init__()
        self.recording = 0
        self.data = []
        self.idt = []

    def handle_starttag(self, tag, attrs):
        if tag != 'a':
            return

        if len(attrs) != 4:
            return

        if "link " not in attrs[3]:
            return

        attribute = attrs[2][1]
        self.idt.append(attribute[attribute.find("j_idt") + 5:attribute.find(":", 140) - 2])

        if self.recording:
            self.recording += 1
            return
        self.recording = 1

    def handle_endtag(self, tag):
        if tag == 'a' and self.recording:
            self.recording -= 1

    def handle_data(self, data):
        if data.strip():
            if self.recording:
                self.data.append(data.strip())


class ViewStateParser(HTMLParser):
    """
    Parse viewstate hidden value
    """

    def __init__(self):
        super().__init__()
        self.recording = 0
        self.data = []

    def handle_starttag(self, tag, attrs):
        if tag != 'input':
            return
        if self.recording:
            self.recording += 1
            return
        for name, value in attrs:
            if name == 'name' and value == 'javax.faces.ViewState':
                self.data.append(attrs[3][1])
                break
        else:
            return

        self.recording = 1

    def handle_endtag(self, tag):
        if tag == 'input' and self.recording:
            self.recording -= 1

    def handle_data(self, data):
        if data.strip():
            if self.recording:
                self.data.append(data.strip())


class PersoException(Exception):
    def __init__(self, raison):
        self.raison = raison

    def __str__(self):
        return self.raison


class Aurion():
    """
    Aurion class allow interraction with https://webaurion.esiee.fr website
    """
    menu_idt = []
    menu_data = []
    viewstate = ""
    session = None

    def __init__(self):
        None

    def connect(self, username, password):
        """
        Create connection on Aurion and set unites_and_groups data

        :param username: Username ESIEE
        :param password: Password
        :return:
        """
        self.session = requests.session()
        login_url = "https://webaurion.esiee.fr/faces/Login.xhtml"
        result = self.session.get(login_url)

        payload = {
            "j_username": username,
            "j_password": password,
        }

        login_url = "https://webaurion.esiee.fr/j_spring_security_check"
        result = self.session.post(
            login_url,
            data=payload,
            headers=dict(referer=login_url, cookies=self.session.cookies["JSESSIONID"])
        )

        viewstate_url = "https://webaurion.esiee.fr/faces/ChoixDonnee.xhtml"
        viewstate = self.session.get(
            viewstate_url,
            headers=dict(referer=viewstate_url, cookies=self.session.cookies["JSESSIONID"])
        )

        parser = ViewStateParser()
        parser.feed(viewstate.text)
        self.viewstate = parser.data[0]

        menu_parser = MenuParser()
        menu_parser.feed(viewstate.text)
        try:
            self.menu_data = menu_parser.data
            self.menu_idt = menu_parser.idt

        except ValueError:
            raise PersoException("Mauvais Identifiants")

    def get_unites_and_groups(self):
        return self.getGroupsFirstPage(self.session, self.viewstate) + self.getGroupsSecondPage(
            self.session,
            self.viewstate)

    def get_marks(self):
        """
        set Marks

        :param session_requests: requests's session
        :param viewstate_value: value of hidden filed viewstate
        :return: return data likes [{"year": YEAR, "unite": UNITE, "name": NAME, "mark": MARK, "coeff": COEFF}, ....]
        """

        idt = self.menu_idt[self.menu_data.index("Mes Notes")]
        url = 'https://webaurion.esiee.fr/faces/ChoixDonnee.xhtml'
        payload = {"form": "form",
                   "formlargeurDivCenter": "1691",
                   "form:headerSubview:j_idt46": "44807",
                   "form:j_idt168-value": "false",
                   "javax.faces.ViewState": self.viewstate,
                   "form:Sidebar:j_idt" + idt: "form:Sidebar:j_idt" + idt  # E2 321 E1 76 BJ6D)jfVu
                   }
        result = self.session.post(
            url,
            headers=dict(referer=url),
            data=payload
        )

        parser = DataParser()
        parser.feed(result.text)

        data = parser.data[2:-1]
        return [{"year": data[i], "unite": data[i + 1], "name": data[i + 2], "mark": data[i + 3], "coeff": data[i + 4]}
                for i in range(0, len(data) - 4)]

    def getGroupsFirstPage(self, session_requests, viewstate_value):
        """
        Get first page of groups

        :param session_requests: requests's session
        :param viewstate_value: value of hidden filed viewstate
        :return: return data likes ["16_E2_ESP_2003_S2_1, ...]
        """
        idt = self.menu_idt[self.menu_data.index("Mes Groupes")]
        url = 'https://webaurion.esiee.fr/faces/ChoixDonnee.xhtml'
        payload = {"form": "form",
                   "formlargeurDivCenter": "1691",
                   "form:headerSubview:j_idt46": "44807",
                   "form:j_idt168-value": "false",
                   "javax.faces.ViewState": viewstate_value,
                   "form:Sidebar:j_idt" + idt: "form:Sidebar:j_idt" + idt  # E2 321 E1 76 BJ6D)jfVu
                   }
        result = session_requests.post(
            url,
            headers=dict(referer=url),
            data=payload
        )

        parser = DataParser()
        parser.feed(result.text)

        return parser.data[2:-1]

    def getGroupsSecondPage(self, session_requests, viewstate_value):
        """
           Get seconde page of groups

           :param session_requests: requests's session
           :param viewstate_value: value of hidden filed viewstate
           :return: return data likes ["16_E2_ESP_2003_S2_1, ...]
        """
        url = 'https://webaurion.esiee.fr/faces/ChoixDonnee.xhtml'
        payload = {"form": "form",
                   "formlargeurDivCenter": "729",
                   "form:headerSubview:j_idt46": "44807",
                   "form:j_idt168-value": "false",
                   "javax.faces.ViewState": viewstate_value,
                   "javax.faces.source": "form:bas",
                   "javax.faces.partial.event": "rich:datascroller:onscroll",
                   "javax.faces.partial.execute": "form:bas @component",
                   "javax.faces.partial.render": "@component",
                   "form:bas:page": "2",
                   "org.richfaces.ajax.component": "form:bas",
                   "form:bas": "form:bas",
                   "rfExt": "null",
                   "AJAX:EVENTS_COUNT": "1",
                   "javax.faces.partial.ajax": "true"
                   }
        result = session_requests.post(
            url,
            headers=dict(referer=url),
            data=payload
        )

        parser = DataParser()
        parser.feed(result.text)
        return parser.data[2:-1]
