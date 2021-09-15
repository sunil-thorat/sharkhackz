import logging, json
import azure.functions as func
from azure_services import CognitiveServicesApi

def main(req: func.HttpRequest) -> func.HttpResponse:

    try:
        req_body     = req.get_json()
        text         = req_body.get('q', None)
    except ValueError:
        text         = req.params.get('q', None)
    if text:
        response = CognitiveServicesApi().detect(text)
        return func.HttpResponse(body=json.dumps(response), mimetype="application/json", status_code=200)
    else:
        return func.HttpResponse(
            "No query param 'q' found.",
            status_code=200
        )
