import logging
import azure.functions as func
import json
from azure_services import CognitiveSearchApi

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body     = req.get_json()
        search_text  = req_body.get('q', None)
        suggester    = req_body.get('suggester', 'sg')
        mode         = req_body.get('mode', 'twoTerms')
        post_tag     = req_body.get('post_tag', '%3A')
        pre_tag      = req_body.get('pre_tag', '%3A')
        min_coverage = req_body.get('min_coverage', 50)
        top          = req_body.get('top', 1)
    except ValueError:
        search_text  = req.params.get('q', None)
        suggester    = req.params.get('suggester', 'sg')
        mode         = req.params.get('mode', 'twoTerms')
        post_tag     = req.params.get('post_tag', '%3A')
        pre_tag      = req.params.get('pre_tag', '%3A')
        min_coverage = req.params.get('min_coverage', 50)
        top          = req.params.get('top', 1) 


    if search_text:
        suggestions = CognitiveSearchApi().autocomplete(search_text=search_text, suggester=suggester, mode=mode, post_tag=post_tag, pre_tag=pre_tag, min_coverage=min_coverage, top=top)
        return func.HttpResponse(body=json.dumps(suggestions), mimetype="application/json",status_code=200)
    else:
        return func.HttpResponse(
             "No query param 'q' found.",
             status_code=200
        )
