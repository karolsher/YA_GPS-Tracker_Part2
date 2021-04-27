import json

firmware = '1.000'
unittest = '200'
integrationtest = '300'
performancetest : '00'

with open("static/js/data.json", "r") as write_json:
    data = json.load(write_json)
    for p in data:
        p['unittest'] = unittest
        p['integrationtest'] = integrationtest
with open("static/js/data.json", "w") as write_json:
    json.dump(data, write_json)

print("Updating Json with new values...")