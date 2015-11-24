import requests
import xmltodict


def run(start, end, keyword):
    start = start.replace("-", "")
    end = end.replace("-", "")
    print("GESIS Extractor: " + start + end + keyword)

    r = requests.get('http://www.vizgr.org/historical-events/search.php?begin_date=' + start + '&end_date=' + end + '&query=' + keyword + '&language=en')
    # print(r.text)
    try:
        result = xmltodict.parse(r.text)
    except:
        result = False
    output = []
    if result:
        for key in result['result']['event']:
            output.append({"title": key["description"], "description": key["description"], "date": key["date"].replace("/", "-") + "T00:00:00Z", "url": 'https://en.wikipedia.org/wiki/' + key["date"][:4]})
    return output
