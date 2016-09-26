import requests
from html.parser import HTMLParser
import json
from datetime import date
from django.conf import settings


def run(start, end, keyword):
    print("Wikipedia Extractor: " + start + " , " + end + " , " + keyword)

    if end is None:
        end = '2099-01-01'

    startDateList = start.split("-")
    endDateList = end.split("-")

    url = "https://en.wikipedia.org/w/api.php?action=query&titles=" + keyword + "&prop=extracts&format=json"
    data = requests.get(url)
    array = data.json()

    try:
        text_id = list(array['query']['pages'].keys())[0]
        wiki_text = array['query']['pages'][text_id]['extract']
        wiki_text = strip_tags(wiki_text)
        headers = {'content-type': 'application/json'}

        result = requests.post(settings.PC_SERVICES['references']['eventminer_url'], data=json.dumps({"text": wiki_text}), headers=headers)
        resultJson = result.json()
        resultJson = resultJson['extraction_result']

        if result:
            resultArray = []
            for event in resultJson:
                date = calculateDate(event)

                dates = createDateLists(event)

                _start = dates[0]
                _end = dates[1]

                valid_dates = validDate(startDateList, endDateList, _start, _end)

                if len(valid_dates) > 0:
                    if date[1] != "":
                        newEvent = {"title": event['event'], "description": event['event'], "url": "https://en.wikipedia.org/wiki/" + keyword, "date": valid_dates[0], "endDate": valid_dates[1]}
                    else:
                        newEvent = {"title": event['event'], "description": event['event'], "url": "https://en.wikipedia.org/wiki/" + keyword, "date": valid_dates[0]}
                    resultArray.append(newEvent)
        return resultArray

    except:
        result = False
        return []


def createDateLists(event):
    start_year = event['start_year']
    start_month = event['start_month']
    start_day = event['start_day']

    end_year = event['end_year']
    end_month = event['end_month']
    end_day = event['end_day']

    _start = [start_year, start_month, start_day]
    _end = [end_year, end_month, end_day]

    return [_start, _end]


def validDate(start, end, _start, _end):
    if _start[0] == "":
        _start[0] = '0001'
    if _start[1] == "":
        _start[1] = '01'
    if _start[2] == "":
        _start[2] = '01'

    if _end[0] == "":
        if end[0] != "2099":
            return []
        else:
            _end[0] = end[0]
    if _end[1] == "":
        _end[1] = end[1]
    if _end[2] == "":
        _end[2] = end[2]

    date_start = date(int(start[0]), int(start[1]), int(start[2]))
    date_end = date(int(end[0]), int(end[1]), int(end[2]))
    _date_start = date(int(_start[0]), int(_start[1]), int(_start[2]))
    _date_end = date(int(_end[0]), int(_end[1]), int(_end[2]))

    if date_start.isoformat() <= _date_start.isoformat() and date_end.isoformat() >= _date_end.isoformat():
        return [_date_start, _date_end]
    else:
        return []


def calculateDate(result):
    startDate = ""
    endDate = ""
    if result['start_day']:
        startDate = startDate + result['start_day'] + "-"
    else:
        startDate = startDate + "01-"

    if result['start_month']:
        startDate = startDate + result['start_month'] + "-"
    else:
        startDate = startDate + "01-"

    if result['start_year']:
        startDate = startDate + result['start_year']
    else:
        startDate = startDate + "0001"

    if result['end_year']:
        if result['end_day']:
            endDate = endDate + result['end_day'] + "-"
        else:
            endDate = endDate + "01-"

        if result['end_month']:
            endDate = endDate + result['end_month'] + "-"
        else:
            endDate = endDate + "01-"

        endDate = endDate + result['end_year']

    return [startDate, endDate]


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
