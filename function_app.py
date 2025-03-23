import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

def handle_request(req: func.HttpRequest) -> str:
    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')
    return name

def log_request():
    logging.info('Python HTTP trigger function processed a request.')

@app.route(route="uml")
def uml(req: func.HttpRequest) -> func.HttpResponse:
    log_request()
    name = handle_request(req)

    status_messages = {
        200: "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response."
    }

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             status_messages[200],
             status_code=200
        )
