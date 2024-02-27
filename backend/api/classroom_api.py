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

    # Retrieve all classroom entity instances from the database
    @app.route("/api/classroom", methods=["GET"])
    def retrieve_classroom():
        sql = "SELECT * FROM CLASSROOM;"
        classroom = execute_read_query(connection, sql)
        return jsonify(classroom)

    # Retrieve a classroom instance by ID
    @app.route("/api/classroom/<int:class_id>", methods=["GET"])
    def retrieve_classroom_id(class_id):
        sql = "SELECT * FROM CLASSROOM;"
        classroom = execute_read_query(connection, sql)

        for entity in classroom:
            if entity["CLASS_ID"] == class_id:
                return jsonify(entity)
        return "Invalid ID"

    # Delete a classroom instance
    @app.route("/api/classroom/<int:class_id>", methods=["DELETE"])
    def delete_class_id(class_id):
        sql = "SELECT * FROM CLASSROOM;"
        classroom = execute_read_query(connection, sql)

        for i in range(len(classroom) - 1, -1, -1):  # start, stop, step size
            id_to_delete = classroom[i]["CLASS_ID"]
            if class_id == id_to_delete:
                delete_statement = f"Successfully deleted {classroom[i]['CLASS_NAME']} from the database"
                delete_query = f"DELETE FROM CLASSROOM WHERE CLASS_ID = {class_id}"
                delete_sql = execute_query(connection, delete_query)
                return delete_statement, delete_sql

        return "Invalid ID"

    # Add a classroom entity
    @app.route("/api/classroom", methods=["POST"])
    def add_classroom():
        request_data = request.get_json()

        if (not request_data) or ("CLASS_ID" in request_data.keys()):
            return "No classroom details provided"

        columns = [key for key in request_data.keys()]

        if (len(columns) > 3) or (len(columns) < 3):
            return "Incomplete data, try again"

        class_capacity = request_data["CLASS_CAPACITY"]
        class_name = request_data["CLASS_NAME"]
        facility_id = request_data["FACILITY_ID"]

        facility_sql = f"SELECT FACILITY_ID FROM FACILITY;"
        facility = execute_read_query(connection, facility_sql)

        # Lists the allowed facilities by ID
        allowed_facilities = [facility[i]["FACILITY_ID"] for i in range(len(facility))]

        if facility_id not in allowed_facilities:
            return "Invalid facility ID"

        add_query = f"INSERT INTO CLASSROOM (CLASS_CAPACITY, CLASS_NAME, FACILITY_ID)" \
                    f"VALUES ({class_capacity}, '{class_name}', {facility_id})"
        execute_query(connection, add_query)

        return "Classroom addition success"

    # Update a classroom entity
    @app.route("/api/classroom/<int:class_id>", methods=["PUT"])
    def update_classroom_id(class_id):
        # Check if the classroom exists in the database
        sql = f"SELECT * FROM CLASSROOM WHERE CLASS_ID = {class_id};"
        check = execute_read_query(connection, sql)
        if not check:
            return "Classroom with the provided ID does not exist"

        request_data = request.get_json()

        sets = []

        if "CLASS_CAPACITY" in request_data.keys():
            class_capacity = request_data["CLASS_CAPACITY"]
            sets.append({"CLASS_CAPACITY": class_capacity})

        if "CLASS_NAME" in request_data.keys():
            class_name = request_data["CLASS_NAME"]
            sets.append({"CLASS_NAME": class_name})

        if "FACILITY_ID" in request_data.keys():
            facility_id = request_data["FACILITY_ID"]

            facility_sql = f"SELECT FACILITY_ID FROM FACILITY;"
            facility = execute_read_query(connection, facility_sql)

            # Lists the allowed facilities by ID
            allowed_facilities = [facility[i]["FACILITY_ID"] for i in range(len(facility))]

            if facility_id in allowed_facilities:
                sets.append({"FACILITY_ID": facility_id})
            else:
                return "Facility does not exist"

        for item in sets:
            for key, value in item.items():
                if isinstance(value, int):
                    update_sql = f"UPDATE CLASSROOM SET {key} = {value} WHERE CLASS_ID = {class_id};"
                else:
                    update_sql = f"UPDATE CLASSROOM SET {key} = '{value}' WHERE CLASS_ID = {class_id};"
                execute_query(connection, update_sql)

        return "Update success"

    app.run()
