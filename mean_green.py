import logging
import datetime

import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

gp_search_url = "https://secure.gpus.org/secure/testdb/search.php"

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def get_gp_candidates_by_filter(filter_year):

    candidates = None

    candidate_request = requests.post(gp_search_url, {"filter_year": filter_year})

    if candidate_request.status_code == 200:
        candidates = {}
        soup = BeautifulSoup(candidate_request.text, 'html.parser')
        for c in soup.body.table.table.table.findAll("tr")[2:]:
            name = c.td.a.text
            candidates[name] = dict()
            for detail in c.findAll("td")[1:][0].get_text("|").split("|"):
                d = detail.split(":", 1)
                candidates[name][d[0].strip()] = d[1].strip()
    else:
        logging.error("Requests for candidates did not respond OK. Response code is <{}>".format(
            candidate_request.status_code))

    return candidates


candidates_2015 = get_gp_candidates_by_filter(filter_year=2015)
candidates_2016 = get_gp_candidates_by_filter(filter_year=2016)

states_2016 = map(lambda c: c['State'], candidates_2016.values())
candidates_2016_by_state = [[x, states_2016.count(x)] for x in set(states_2016)]

offices_2016 = map(lambda c: c['Office'], candidates_2016.values())
candidates_2016_by_offices = [[x, offices_2016.count(x)] for x in set(offices_2016)]

candidates_2016_that_ran_in_2015 = list(set(candidates_2015.keys()) & set(candidates_2016.keys()))

print "# Analytics about the 2016 Green Party"
print "## Run at {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
print "## Based on election database at [Green Party 2016 candidates](http://www.gp.org/2016_candidates)"
print "\n"
print tabulate(candidates_2016_by_offices, headers=['Office', 'Count'], tablefmt="pipe")
print "\n"
print tabulate(candidates_2016_by_state, headers=['State', 'Count'], tablefmt="pipe")
print "\n"
print tabulate(map(lambda c: [c], candidates_2016_that_ran_in_2015), headers=['Also ran in 2015'], tablefmt="pipe")


