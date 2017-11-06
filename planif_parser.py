"""
Project : ade-esiee
File : plani_parser
Author : DELEVACQ Wallerand
Date : 01/10/17
"""
import urllib.request
import urllib.error
from html.parser import HTMLParser

import requests
from icalendar import Calendar, Event

class UnitePlanifParser(HTMLParser):
    """
    Parse unite id
    """

    def __init__(self):
        super().__init__()
        self.recording = 0
        self.data = []
        self.idt = []

    def handle_starttag(self, tag, attrs):
        if tag != 'a':
            return

        if len(attrs) != 1:
            return

        href = attrs[0][1]
        href = href[href.find(",")+1:href.find(")")]

        if "'" not in href:
            try:
                if int(href) not in self.idt:
                    self.idt.append(int(href))
            except ValueError as e:
                pass

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


def get_planif_link(username, password):
    session = requests.session()

    url = "https://planif.esiee.fr/jsp/custom/esiee/easyMyPlanning.jsp"
    result = session.get(url)

    url = "https://planif.esiee.fr/jsp/custom/esiee/easyMyPlanning/connect.jsp"
    payload = {
        "login": username,
        "password": password,
    }
    result = session.post(url, data=payload, headers=dict(referer=url, cookies=session.cookies["JSESSIONID"]))

    url = "https://planif.esiee.fr/jsp/custom/esiee/easyMyPlanning/selectResources.jsp?reset&projectId=7"
    result = session.get(url, headers=dict(referer=url, cookies=session.cookies["JSESSIONID"]))

    parser = UnitePlanifParser()
    parser.feed(result.text)

    idt = parser.idt

    url = "https://planif.esiee.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?resources="

    for id in idt:
        url+=str(id)+","

    url+="&projectId=7&calType=ical&nbWeeks=12"

    return url

def download_ics_from_planif():
    url = "https://planif.esiee.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?resources=147,738,739,743,744,2841,5757,746,747,748,2781,2782,3286,682,683,684,685,659,665,674,680,681,727,733,785,998,1295,2555,2743,5215,5688,731,734,735,736,740,741,742,780,782,1852,2584,4350,5321,786,787,788,789,790,2270,2275,2277,2278,2282,704,745,773,775,776,4937,728,2117,772,719,2112,183,185,196,4051,4679,2072,2074,2272,2276,2089,154,713,163,167,700,701,705,707,708,712,714,715,716,724,725,726,737,749,758,759,1057,1858,1908,2090,2108,2281,428,717,720,721,722,2265,2274,2279&projectId=7&calType=ical&nbWeeks=12"

    #url = "https://planif.esiee.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?resources=47,171,3312,3313,3314,215,226,690,2844,3169,3171,3172,3173,2267,3174,979,216,225,5597,949,1017,597,598,&projectId=7&calType=ical&nbWeeks=12"

    try:
        html_data = urllib.request.urlopen(url)
        g = html_data.read().decode('utf8')
        # result = json.loads(data)
        # self.all_cours = [elt for elt in result]

        with open("ADECal.ics", "w") as file:
            file.write(g)

    except urllib.error.URLError as e:
        print(e)

def str_to_date(str):
    return str[0:4]+"-"+str[4:6]+"-"+str[6:8]+str[8]+str[9:11]+":"+str[11:13]+":"+str[13:15]+".000Z"

def ics_to_json_from_ade():
    events_list = []

    with open("ADECal.ics", "r") as g:
        gcal = Calendar.from_ical(g.read())
        for component in gcal.walk():
            if component.name == "VEVENT":
                events_list.append(dict(description=str(component.get("DESCRIPTION")),
                                        end=(str_to_date(str(component.get("DTEND").to_ical().decode("utf-8")))),
                                        start=(str_to_date(str(component.get("DTSTART").to_ical().decode("utf-8")))),
                                        name=str(component.get("SUMMARY")),
                                        rooms=(component.get("LOCATION").replace(" ", "")).split(",")))
    return events_list


if __name__ == "__main__":
    #download_ics_from_planif()
    #print(ics_to_json_from_ade()[0])
    #print(get_planif_link())
    pass
