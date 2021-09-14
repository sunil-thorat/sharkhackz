import logging
import azure.functions as func
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
import json
import os

osenv = os.environ
config = {
    "search_service_name": osenv.get('SearchServiceName', "mix"),
    "search_api_key": osenv.get('SearchApiKey', "ABF7920FCE83D3B4CA63947C7FDCE13F"),
    "search_index_name": osenv.get('SearchIndexName', "cosmosdb-index"),
}

endpoint = f'https://{config.get("search_service_name")}.search.windows.net'
key = config.get("search_api_key")
index_name = config.get("search_index_name")

# Create Azure SDK client
search_client = SearchClient(endpoint, index_name, AzureKeyCredential(key))

def main(req: func.HttpRequest) -> func.HttpResponse:
    # variables sent in body
    req_body = req.get_json()
    q = req_body.get('q')
    top = req_body.get('top')
    suggester = req_body.get('suggester')

    if q:
        logging.info(f"/auto-complete q = {q}")
        suggestions = search_client.autocomplete(search_text=q, suggester_name=suggester, mode="oneTermWithContext", minimum_coverage=50)
        
        # format the React app expects
        full_response = {}
        full_response["suggestions"]=suggestions
        
        return func.HttpResponse(body=json.dumps(full_response), mimetype="application/json", status_code=200)
    else:
        return func.HttpResponse(
             "No query param found.",
             status_code=200
        )
