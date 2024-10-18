from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flasgger import Swagger

import book_review

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

class UppercaseText(Resource):
    """
    Handles HTTP GET requests by converting text input to uppercase and returning
    it in JSON format.

    """
    def get(self):
        """
        Handles HTTP GET requests by retrieving a 'text' parameter from the request
        query string, converting it to uppercase, and returning it as a JSON response.

        Returns:
            Dict[str,str]: Converted to a JSON response.

        """
        text = request.args.get('text')

        return jsonify({"text": text.upper()})
    
class Records(Resource):
    """
    Handles HTTP GET requests to retrieve a list of books from a database. It
    accepts optional query parameters 'count' and 'sort', allowing users to customize
    the number of books returned and their sorting order.

    """
    def get(self):
        """
        Handles HTTP GET requests to retrieve a list of book records. It accepts
        optional query parameters 'count' and 'sort', which determine the number
        of records returned and the sorting order, respectively.

        Returns:
            Dict[str,Any]: A dictionary containing a key "books" with a value of
            type List[Any] which is a list of books and a status code 200.

        """

        count = request.args.get('count')  # Default to returning 10 books if count is not provided
        sort = request.args.get('sort')

        # Get all the books
        books = book_review.get_all_records(count=count, sort=sort)

        return {"books": books}, 200
    
class AddRecord(Resource):
    """
    Handles HTTP POST requests to add a new record to a database table. It expects
    a JSON body containing 'Book' and 'Rating' fields. If valid, it calls the
    `add_record` function to add the record, returning success or failure messages
    accordingly.

    """
    def post(self):
        """
        Handles HTTP POST requests to add a new record to the database. It expects
        the request body to contain 'Book' and 'Rating' keys, validates their
        presence, and calls the `add_record` function to add the record.

        Returns:
            Dict[str,int|str]: A dictionary containing a message and a status code.

        """

        data = request.json
        print(data)

        # Check if 'Book' and 'Rating' are present in the request body
        if 'Book' not in data or 'Rating' not in data:
            return {"message": "Bad request, missing 'Book' or 'Rating' in the request body"}, 400
        # Call the add_record function to add the record to the DB table
        success = book_review.add_record(data)

        if success:
            return {"message": "Record added successfully"}, 200
        else:
            return {"message": "Failed to add record"}, 500
        


api.add_resource(AddRecord, "/add-record")
api.add_resource(Records, "/records")
api.add_resource(UppercaseText, "/uppercase")

if __name__ == "__main__":
    app.run(debug=True)