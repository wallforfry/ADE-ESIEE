"""
Project : ADE-ESIEE
File : unites_api.py
Author : DELEVACQ Wallerand
Date : 23/05/2017
"""
import csv
from html.parser import HTMLParser

class UnitesParser(HTMLParser):
    """
    Parse data unites intra website
    """

    def __init__(self):
        super().__init__()
        self.recording = 0
        self.data = []
        self._data = ""
        self._starttag = None

    def handle_starttag(self, tag, attrs):
        if tag != 'font':
            return
        self._starttag = tag

    def handle_data(self, data):
        self._data = data

    def handle_endtag(self, tag):
        if self._starttag == "font":
            self.data.append(self._data)
        self._data = ""
        self._starttag = None


def generate_csv_file(row):
    """
    Generate csv file from the row
    :param row: Row of the web site
    :return: None
    """

    parser = UnitesParser()
    parser.feed(row)
    data = parser.data

    with open('unites.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for i in range(2, len(data), 9):
            writer.writerow(
                [data[i + 1].replace("\n", "").replace("\t", ""), data[i + 2].replace("\n", "").replace("\t", ""),
                 data[i + 3].replace("\n", "").replace("\t", ""), data[i + 4].replace("\n", "").replace("\t", ""),
                 data[i + 5].replace("\n", "").replace("\t", ""), data[i + 6].replace("\n", "").replace("\t", ""),
                 data[i + 7].replace("\n", "").replace("\t", "")])

    return None


def get_row_on_website():
    """
    Return row of website
    :return: All row of the website
    """

    """url = 'https://extra.esiee.fr/intranet/consultation_brochures/index.php'
    payload = {"s_annee_scolaire": "",
               "s_pays": "FRA",
               "s_ecole": "",
               "s_id_laboratoire": "",
               "s_cursus": "",
               "unite": "",
               "affichage": "0",
               "b_rechercher": "Rechercher"
               }
    result = requests.session().post(
        url,
        headers=dict(referer=url),
        data=payload
    )

    result = None
    """
    #Encodage for linux server only
    with open("site.html", encoding="iso-8859-1", mode="r") as f:
    #Encodage for windows
    #with open("site.html", mode="r") as f:
        result = f.read()

    return result


def search_unite(unite_code):
    """
    Search unite in csv file and get its natural name
    :param unite_code: Code like "IGI-2102"
    :return: "Name of the unite"
    """
    with open("unites.csv") as f:
        csv_file = csv.reader(f, delimiter=",")
        for row in csv_file:
            # if current rows 2nd value is equal to input, print that row
            if unite_code == row[1]:
                return row[2]


if __name__ == "__main__":
    result = get_row_on_website()
    generate_csv_file(result)
