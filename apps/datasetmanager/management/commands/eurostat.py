from django.core.management.base import BaseCommand
from django.apps import apps as django_apps
from collections import OrderedDict
from django.conf import settings
from pandasdmx import Request
import json
import requests
import datetime


class Command(BaseCommand):
    help = 'Eurostat'

    def handle(self, *args, **options):
        # if all datasets should be downloaded
        if len(args) == 1 and args[0] == 'ALL':
            # usage of pandasdmx
            estat = Request("ESTAT")
            dataflow = estat.get(resource_type='dataflow')
            dataflows = dataflow.msg.dataflows
            args = dataflows.keys()

        # iterate over every Eurostat code in arguments
        for code in args:
            filters = []
            query = " "
            filters_description = ""

            data = requests.get("http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/" + str(code) + "?precision=1")

            # selection of filters
            if data.status_code == 416:
                # usage of pandasdmx
                estat = Request("ESTAT")
                dataflow = estat.get(resource_type='dataflow')
                dataflows = dataflow.msg.dataflows
                dsd_id = dataflows[code].structure.id
                dsd_resp = estat.get(resource_type='datastructure', resource_id=dsd_id)
                dsd = dsd_resp.msg.datastructures[dsd_id]
                dimensionsList = list(dsd.dimensions)

                # choose first option of any filter, except TIME_PERIOD, GEO and FREQ
                for f in range(0, len(dimensionsList)):
                    if(dimensionsList[f] != "TIME_PERIOD" and dimensionsList[f] != "GEO" and dimensionsList[f] != "FREQ"):
                        dimensionsValuesList = list(dsd.dimensions[dimensionsList[f]].local_repr.enum.values())
                        filters.append([dimensionsList[f], [dimensionsValuesList[0].id]])
                        filters_description += dimensionsList[f] + ": " + dimensionsValuesList[0].name.en + ", "

                if(filters):
                    for key in range(0, len(filters)):
                        for value in range(0, len(filters[key][1])):
                            query += '&' + filters[key][0].lower() + '=' + filters[key][1][value]

                # new request with selected filters
                data = requests.get("http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/" + str(code) + "?precision=1" + query.strip())

            try:
                array = data.json(object_pairs_hook=OrderedDict)
                # get countries
                rowHeaders = array['dimension']['geo']['category']['label']
                rowHeadersValues = list(rowHeaders.values())
                rowLen = len(rowHeadersValues)
                # get years
                colHeaders = array['dimension']['time']['category']['label']
                colHeadersVals = list(colHeaders.values())
                colLen = len(colHeadersVals) + 1
                colHeadersValues = []
                colHeadersValues.append("")

                for q in range(0, colLen - 1):
                    colHeadersValues.append(colHeadersVals[q])

                val = array['value']
                values = list(val.values())
                rowArrays = []
                index = 0

                for row in range(0, rowLen):
                    colArray = []
                    position = row * (colLen - 1)
                    colArray.append(rowHeadersValues[row])
                    for col in range(0, colLen - 1):
                        if val.get(str(position + col)) is None:
                            colArray.append("")
                        else:
                            colArray.append(values[index])
                            index += 1

                    rowArrays.append(colArray)

                Individual = django_apps.get_model("referencepool", "Individual")
                individuals_list = Individual.objects.all()

                DataClass = django_apps.get_model("referencepool", "DataClass")
                data_class = DataClass.objects.get(title="Country")

                Indicator = django_apps.get_model("indicatorservice", "Indicator")

                try:
                    new_indicator = Indicator.objects.get(name=array['label'])
                except:
                    new_indicator = Indicator(name=array['label'], description=array['label'])
                    new_indicator.save()

                spatials = []

                # choose already existing individuals from referencepool or create missing individuals
                for i in range(0, len(rowHeaders)):
                    spatial_key = list(rowHeaders.keys())[i]
                    spatial_value = list(rowHeaders.values())[i]
                    found = False
                    for individual in individuals_list:
                        if spatial_value == individual.title:
                            spatials.append(individual.id)
                            found = True

                    if found is False:
                        new_individual = Individual(title=spatial_value, code=spatial_key, data_class=data_class)
                        new_individual.save()
                        spatials.append(new_individual.id)

                resultArray = []

                # create result array in correct format
                for row in range(0, len(rowArrays)):
                    values = {}
                    spatial = ""
                    for individual in individuals_list:
                        if rowArrays[row][0] == individual.title:
                            spatial = individual.title

                    for i in range(1, len(colHeadersValues)):
                        if type(rowArrays[row][i]) is str:
                            values[colHeadersValues[i]] = None
                        else:
                            values[colHeadersValues[i]] = rowArrays[row][i]

                    resultArray.append({"row": row + 1, "individual": spatial, "values": values})

                # headers for POST request
                headers = {'content-type': 'application/json', 'x-user-path': 'https://adhocracy-prod.policycompass.eu/api/principals/users/0000072/', 'x-user-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpYXQiOjE0Nzg1Mjg2NDIsInN1YiI6Ii9wcmluY2lwYWxzL3VzZXJzLzAwMDAwNzIiLCJleHAiOjE0ODExMjA2NDJ9.HhV3dnlZp_B_A0q6Ijq7MMwC8tbcDMz72ZqP2XW9WCumLZVVoMoGSaxk7CyZkC-F4jSHrx4htn9h5ZqOx35l3Q'}

                # prepare new dataset
                payload = {}
                payload['time'] = {"resolution": "year", "start": colHeadersValues[1], "end": colHeadersValues[len(colHeadersValues) - 1]}
                payload["resource"] = {"issued": datetime.datetime.today().strftime('%Y-%m-%d'), "external_resource": 71, "url": "http://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=" + str(code) + "&lang=en"}
                payload["policy_domains"] = [1]
                payload["title"] = array['label']
                payload["keywords"] = array['label']
                payload["license_id"] = 96
                payload["description"] = array['label']
                payload["spatials"] = spatials
                payload["language_id"] = 38
                payload["indicator_id"] = new_indicator.id
                payload["class_id"] = 1
                payload["user_id"] = 1
                payload["unit_id"] = 25
                payload["data"] = {"table": resultArray}
                payload["is_draft"] = False

                # add selected filters to description
                if len(filters) > 0:
                    payload['description'] = payload['description'] + " (selected filters: " + filters_description[:-2] + ")"

                requests.post(settings.PC_SERVICES['references']['base_url'] + '/api/v1/datasetmanager/datasets', data=json.dumps(payload), headers=headers)
                print("Download of '", code, "' successful")

            except:
                print("ERROR: Download of '", code, "' unsuccessful")
