import logging

import requests
from bs4 import BeautifulSoup

gp_search_url = "https://secure.gpus.org/secure/testdb/search.php"

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def get_gp_canidates_by_filter(filter_year, deep_get=False):

    canidates = None

    canidate_request = requests.post(gp_search_url, {"filter_year": filter_year})

    if canidate_request.status_code == 200:
        canidates = []
        soup = BeautifulSoup(canidate_request.text, 'html.parser')
        for c in soup.body.table.table.table.findAll("tr")[2:]:
            canidate = dict()
            canidate["name"] = c.td.a.text
            for detail in c.findAll("td")[1:][0].get_text("|").split("|"):
                d = detail.split(":", 1)
                canidate[d[0].strip()] = d[1].strip()
            canidates.append(canidate)
    else:
        logging.error("Requests for canidates did not respond OK. Response code is <%{}>".format(
            canidate_request.status_code))

    return canidates


canidates_2015 = get_gp_canidates_by_filter(filter_year=2015)
canidates_2016 = get_gp_canidates_by_filter(filter_year=2016)

count_2016 = 0
for canidate in canidates_2016:
    if canidate['Elected'] != 'No':
        count_2016 +=1

print count_2016