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

        if "FACILITY_ID" in request_data.keys():
            return "Cannot manually add facility ID"

        allowed_keys = ["FACILITY_NAME"]
        retrieved_keys = [key for key in request_data.keys()]

        # If you put a key other than what's in allowed_keys such as JOB_CODE OR EMPLOYEE_CODE, then an error will show
        for key in retrieved_keys:
            if key not in allowed_keys:
                return f"Invalid key(s) not allowed\n" \
                       f"Keys must be: {', '.join(allowed_keys)}"

        # Since every columns (keys) are NOT NULL (WE NEED THEM), if one is missing from allowed_keys, error is shown
        # Postman will also tell you which columns (keys) you're missing
        if len(retrieved_keys) != len(allowed_keys):
            missing_keys = []
            for key in allowed_keys:
                if key not in retrieved_keys:
                    missing_keys.append(key)
            if len(missing_keys) > 1:
                return f"Error: Insufficient data. make sure {', '.join(missing_keys)} are included"
            else:
                return f"Error: Insufficient data. make sure {' '.join(missing_keys)} is included"

        # Assign variables to their corresponding data type; if not met, throw an error
        try:
            facility_name = str(request_data["FACILITY_NAME"])
        except ValueError:
            return "Facility name must be string"

        add_query = f"INSERT INTO FACILITY (FACILITY_NAME) VALUES ('{facility_name}');"
        execute_query(connection, add_query)

        return "Facility Addition Success"

    # Update a facility entity
    @app.route("/api/facility/<int:facility_id>", methods=["PUT"])
    def update_facility_id(facility_id):
        request_data = request.get_json()
        # Check if the facility exists in the database
        sql = f"SELECT * FROM FACILITY WHERE FACILITY_ID = {facility_id};"
        check = execute_read_query(connection, sql)
        if not check:
            return "Facility with the provided ID does not exist"

        if "FACILITY_ID" in request_data.keys():
            return "Cannot manually add facility ID"

        allowed_keys = ["FACILITY_NAME"]
        retrieved_keys = [key for key in request_data.keys()]

        # If you put a key other than what's in allowed_keys such as JOB_CODE OR EMPLOYEE_CODE, then an error will show
        for key in retrieved_keys:
            if key not in allowed_keys:
                return f"Invalid key(s) not allowed\n" \
                       f"Keys must be: {', '.join(allowed_keys)}"

        facility_name = request_data["FACILITY_NAME"]

        sql = f"UPDATE FACILITY SET FACILITY_NAME = '{facility_name}' WHERE FACILITY_ID = {facility_id}"
        execute_query(connection, sql)

        return "Update success"

    app.run()
