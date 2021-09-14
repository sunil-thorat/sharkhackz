import logging
import azure.functions as func
import json
from azure_services import CognitiveSearchApi


def main(req: func.HttpRequest) -> func.HttpResponse:
    # variables sent in body
    req_body = req.get_json()
    q = req_body.get('q')
    top = req_body.get('top')
    suggester = req_body.get('suggester')

    if q:
        logging.info(f"/suggest q = {q}")
        suggestions = search_client.suggest(search_text=q, suggester_name=suggester, top=top)
        
        # format the React app expects
        full_response = {}
        full_response["suggestions"]=suggestions
        
        return func.HttpResponse(body=json.dumps(full_response), mimetype="application/json",status_code=200)
    else:
        return func.HttpResponse(
             "No query param found.",
             status_code=200
        )
