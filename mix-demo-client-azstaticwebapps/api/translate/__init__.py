import logging, json
import azure.functions as func
from azure_services import CognitiveServicesApi

# https://docs.microsoft.com/en-us/rest/api/cognitiveservices/translator/translator/translate
def main(req: func.HttpRequest) -> func.HttpResponse:

    try:
        req_body     = req.get_json()
        text         = req_body.get('q', None)
        src_lang     = req_body.get('from', None)
        dest_lang    = req_body.get('to', 'en')
    except ValueError:
        text         = req.params.get('q', None)
        src_lang     = req.params.get('from', None)
        dest_lang    = req.params.get('to', 'en')

    if src_lang == '' or src_lang == 'undefined':
        src_lang = None

    if text:
        response = CognitiveServicesApi().translate(text, src_lang=src_lang, dest_lang=dest_lang)
        return func.HttpResponse(body=json.dumps(response), mimetype="application/json", status_code=200)
    else:
        return func.HttpResponse(
            "No query param 'q' found.",
            status_code=200
        )
