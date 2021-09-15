import os
import logging
import json
import uuid
import requests
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

osenv = os.environ
config = {
    "search_service_name": osenv.get('SearchServiceName', "mix"),
    "search_api_key": osenv.get('SearchApiKey', "CEA73D8D544B23CA84E15EC26936ED62"),
    "search_index_name": osenv.get('SearchIndexName', "hotels-sample-index"),
    "cs_region": osenv.get('CognitiveServicesRegion', "CentralUS"),
    "cs_subscription_key": osenv.get('CognitiveServicesSubscriptionKey', "44231fa2339147fab1d62941079f9ab4"),
    "cs_endpoint_url": osenv.get('CognitiveServicesEndpointName', "https://api.cognitive.microsofttranslator.com")
}

logger = logging.getLogger('mixclient')
logger.setLevel(logging.DEBUG)

class CognitiveServicesApi:
    def __init__(self):
        self.subscription_key = config.get("cs_subscription_key")
        self.endpoint_url = config.get("cs_endpoint_url")
        self.region = config.get("cs_region")
        self.headers =  {
            'Ocp-Apim-Subscription-Key': self.subscription_key,
            'Content-Type': 'application/json; charset=UTF-8',
            'Ocp-Apim-Subscription-Region': self.region,
            'X-ClientTraceId': str(uuid.uuid4())
        } 

    def translate(self, text, dest_lang='en', src_lang=None):
        print(text)
        url = self.endpoint_url + '/translate'
        req_body = [
            {
                "text": text
            }
        ]
        params = {"api-version": "3.0"}
        if src_lang:
            params['from'] = src_lang
        params['to'] = [dest_lang]

        try:
            response = requests.post(url, params=params, headers=self.headers, json=req_body)
        except Exception as ex:
            logger.exception(ex)

        full_response = {}
        if response.status_code == 200:
            full_response["detectedLanguage"] = response.json()[0]["detectedLanguage"]["language"]
            full_response["translated_text"] = response.json()[0]["translations"][0]["text"]

        return full_response

    def detect(self, text):
        url = self.endpoint_url + '/detect'
        req_body = [
            {
                "text": text
            }
        ]
        params = {"api-version": "3.0"}
        try:
            response = requests.post(url, params=params, headers=self.headers, json=req_body)
        except Exception as ex:
            logger.exception(ex)

        if response.status_code == 200:
            return response.json()[0]
        return {}

class CognitiveSearchApi:
    def __init__(self):
        self.endpoint = f'https://{config.get("search_service_name")}.search.windows.net'
        self.api_key = config.get("search_api_key")
        self.index_name = config.get("search_index_name")
        self.search_client = SearchClient(self.endpoint, self.index_name, AzureKeyCredential(self.api_key))

    def suggest(self, search_text, suggester, post_tag, pre_tag, min_coverage, order_by, top):
        suggestions = self.search_client.suggest(search_text=search_text, suggester_name=suggester, highlight_post_tag=post_tag, highlight_pre_tag=pre_tag, minimum_coverage=min_coverage, order_by=order_by, top=top)
        full_response = {}
        if suggestions:
            full_response["suggestions"] = suggestions
        return full_response

    def autocomplete(self, search_text, suggester, mode, post_tag, pre_tag, min_coverage, top):
        suggestions = self.search_client.autocomplete(search_text=search_text, suggester_name=suggester, mode=mode, highlight_post_tag=post_tag, highlight_pre_tag=pre_tag, minimum_coverage=min_coverage, top=top)
        full_response = {}
        if suggestions:
            full_response["suggestions"] = suggestions
        return full_response
        