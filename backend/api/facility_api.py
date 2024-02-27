import flask
from flask import jsonify, request
from self_made_modules.sql_helper import create_connection, execute_read_query, execute_query
from self_made_modules import creds


if __name__ == "__main__":
    # setting up an application name
    app = flask.Flask(__name__)  # sets up the application
    app.config["DEBUG"] = True  # allow to show errors in browser

    my_creds = creds.Creds()
    connection = create_connection(my_creds.connection_string,
                                   my_creds.user_name,
                                   my_creds.password,
                                   my_creds.database_name)

    # Retrieve all facility entity instances from the database
    @app.route("/api/facility", methods=["GET"])
    def retrieve_facility():
        sql = "SELECT * FROM FACILITY;"
        facility = execute_read_query(connection, sql)
        return jsonify(facility)

    # Retrieve a facility instance by ID
    @app.route("/api/facility/<int:facility_id>", methods=["GET"])
    def retrieve_facility_id(facility_id):
        sql = "SELECT * FROM FACILITY"
        facility = execute_read_query(connection, sql)

        for entity in facility:
            if entity["FACILITY_ID"] == facility_id:
                return jsonify(entity)
        return "Invalid ID"

    # Delete a faculty instance
    @app.route("/api/facility/<int:facility_id>", methods=["DELETE"])
    def delete_faculty_id(facility_id):
        sql = "SELECT * FROM FACILITY;"
        facility = execute_read_query(connection, sql)

        for i in range(len(facility) - 1, -1, -1):  # start, stop, step size
            id_to_delete = facility[i]["FACILITY_ID"]
            if facility_id == id_to_delete:
                delete_statement = f"Successfully deleted {facility[i]['FACILITY_NAME']} from the database"
                delete_query = f"DELETE FROM FACILITY WHERE FACILITY_ID = {facility_id}"
                delete_sql = execute_query(connection, delete_query)
                return delete_statement, delete_sql

        return "Invalid ID"

    # Add a facility entity
    @app.route("/api/facility", methods=["POST"])
    def add_facility():
        request_data = request.get_json()

        if not request_data:
            return "No facility name provided"

        facility_name = request_data["FACILITY_NAME"]
        add_query = f"INSERT INTO FACILITY (FACILITY_NAME) VALUES ('{facility_name}');"
        execute_query(connection, add_query)

        return "Facility Addition Success"

    # Update a facility entity
    @app.route("/api/facility/<int:facility_id>", methods=["PUT"])
    def update_facility_id(facility_id):
        # Check if the facility exists in the database
        sql = f"SELECT * FROM FACILITY WHERE FACILITY_ID = {facility_id};"
        check = execute_read_query(connection, sql)
        if not check:
            return "Facility with the provided ID does not exist"

        request_data = request.get_json()
        facility_name = request_data["FACILITY_NAME"]

        sql = f"UPDATE FACILITY SET FACILITY_NAME = '{facility_name}' WHERE FACILITY_ID = {facility_id}"
        execute_query(connection, sql)

        return "Update success"

    app.run()
