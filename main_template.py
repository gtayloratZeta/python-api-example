from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flasgger import Swagger

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

class UppercaseText(Resource):

    """
    Handles HTTP GET requests to convert input text to uppercase. It retrieves
    text from the request arguments, converts it to uppercase using the `upper()`
    method, and returns the result as a JSON response.

    """
    def get(self):
        """
        Handles HTTP GET requests by retrieving a query parameter named 'text'
        from the request arguments. It then converts the retrieved text to uppercase
        and returns it as a JSON response.

        Returns:
            Dict[str,str]: Converted to a JSON response containing a dictionary
            with a single key-value pair: "text" and the input string in uppercase.

        """
        text = request.args.get('text')

        return jsonify({"text": text.upper()})

api.add_resource(UppercaseText, "/uppercase")

if __name__ == "__main__":
    app.run(debug=True)