
from key_cloak_token import *
import requests
import json
kt = KeyCloakToken()
# kt.get_access_token()


class GetSampleClient:


    def __init__(self):
        self.url = "https://mix.nuance.com/v3/nlu/api/v1/nlu/{}?start=0&end=50&auto=false"

    def get_samples(self, project_id):
        self.url = str(self.url).format(project_id)
        samples = requests.get(self.url, headers={"Authorization":"Bearer "+kt.get_access_token()})
        samples = [sm['literal'] for sm in json.loads(samples.content)['results']]
        print(samples)
        # records = {"samples":samples}
        records = []
        id  = 1
        for s in samples:
            records.append({"id":id, "sample":s})
            id = id + 1

        return records
gs = GetSampleClient()

print(gs.get_samples(project_id="14975"))
