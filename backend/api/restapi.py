import flask
from flask import jsonify, request
from sql_helper import create_connection, execute_read_query, execute_query
import creds


if __name__ == "__main__":
    # setting up an application name
    app = flask.Flask(__name__)  # sets up the application
    app.config["DEBUG"] = True  # allow to show errors in browser

    # Retrieve inventory entity set from database
    my_creds = creds.Creds()
    connection = create_connection(my_creds.connection_string,
                                   my_creds.user_name,
                                   my_creds.password,
                                   my_creds.database_name)

    # Default URL without any routing
    @app.route('/', methods=["GET"])
    def home():
        return "<h1><center>Welcome to the School API</center></h1>"

    # Retrieve all facility objects from the database
    @app.route("/api/facility", methods=["GET"])
    def retrieve_facility():
        sql = "SELECT * FROM FACILITY;"
        facility = execute_read_query(connection, sql)
        return jsonify(facility)

    # Retrieve facility instances by ID
    @app.route("/api/facility/<int:facility_id>")
    def retrieve_facility_id(facility_id):
        sql = "SELECT * FROM FACILITY"
        facility = execute_read_query(connection, sql)

        for entity in facility:
            if entity["FACILITY_ID"] == facility_id:
                return jsonify(entity)
        return "Invalid ID"

    app.run()
