import json
import logging
from flask import Flask, request, jsonify, Response
# Import the function from our separate file
from SchemaConverter import convert_xsd_string_to_openapi

# 1. Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("FlaskApp")

app = Flask(__name__)

@app.route('/convertXmltoJson', methods=['POST'])
def convert_route():
    logger.info("Received request on /convert endpoint.")
    
    try:
        # Get raw XML body from request
        xsd_content = request.get_data(as_text=True)
        
        if not xsd_content or not xsd_content.strip():
            logger.error("Request body is empty or whitespace only.")
            return jsonify({"error": "Empty request body. Please provide valid XSD content."}), 400

        # Call the core logic
        try:
            result_dict = convert_xsd_string_to_openapi(xsd_content)
        except ValueError as ve:
            return jsonify({"error": "Validation Error", "details": str(ve)}), 400
        except RuntimeError as re:
            return jsonify({"error": "Processing Error", "details": str(re)}), 500

        # Convert dictionary to JSON string
        json_output = json.dumps(result_dict, indent=4)
        
        logger.info("Returning JSON response.")
        return Response(json_output, mimetype='application/json')

    except Exception as e:
        logger.exception("Critical server error.")
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)