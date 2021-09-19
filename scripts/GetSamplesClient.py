
from key_cloak_token import *
import requests
import json
kt = KeyCloakToken()
# kt.get_access_token()


class GetSampleClient:


    def __init__(self):
        self.url = "https://mix.nuance.com/v3/nlu/api/v1/nlu/{}?start=0&end=250&auto=false"

    def get_samples(self, project_id):
        self.url = str(self.url).format(project_id)
        samples = requests.get(self.url, headers={"Authorization":"Bearer "+kt.get_access_token()})
        samples = [sm['literal'] for sm in json.loads(samples.content)['results']]
        print(samples)
        literals = self.get_literals(project_id)
        # records = {"samples":samples}
        records = []
        samples = samples + literals
        id  = 1
        for s in samples:
            records.append({"id":id, "sample":s})
            id = id + 1
        print(len(records))
        return records

    def get_literals(self, project_id):
        access_token = kt.get_access_token()
        get_concepts_url = "https://mix.nuance.com/v3/nlu/api/v1/ontology/{}/concepts?locale=en_US".format(project_id)
        get_literal_url_formate = "https://mix.nuance.com/v3/nlu/api/v1/semantic/{}/patterns/{}?size=50&offset=0&sort=VALUE&order=ASC&locale=en_US"
        concepts = requests.get(get_concepts_url, headers={"Authorization": "Bearer " + access_token})
        concepts = [name['name'] for name in json.loads(concepts.content)['data'] if name['type']=='literals']
        literals_final = []
        for c in concepts:
            get_literal_url = get_literal_url_formate.format(project_id, c)
            literals = requests.get(get_literal_url, headers={"Authorization": "Bearer " + access_token})
            [literals_final.append(i['literal']) for i in json.loads(literals.content)['data']['results']]
        return literals_final




gs = GetSampleClient()

print(gs.get_samples(project_id="20523"))
