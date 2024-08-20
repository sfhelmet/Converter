import functions_framework
import service
from flask import jsonify


LANGUAGES = {'Prolog', 'PlantUML', 'Mermaid'}

@functions_framework.http
def transform(request):
    """HTTP Cloud Function to translate code.
    Args:
        request (flask.Request): The request object.
    Returns:
        A JSON response indicating success or failure.
    """
    request_json = request.get_json(silent=True)

    # Ensure the request method is POST
    if request.method != 'POST':
        return jsonify({"error": "Only POST requests are allowed."}), 405

    # Check if the necessary keys are in the JSON payload
    if not request_json:
        return jsonify({"error": "Invalid or missing JSON payload."}), 400

    input_language = request_json.get('input_language')
    output_language = request_json.get('output_language')
    code = request_json.get('code')
    
    if not input_language:
        return jsonify({"error": "input_language is a mandatory field."}), 400
    if not output_language:
        return jsonify({"error": "output_language is a mandatory field."}), 400
    if not code:
        return jsonify({"error": "code is a mandatory field."}), 400
    if input_language not in LANGUAGES:
        return jsonify({"error": "Invalid input_language."}), 400
    if output_language not in LANGUAGES:
        return jsonify({"error": "Invalid output_language."}), 400

    return service.transform(input_language, output_language, code), 200
