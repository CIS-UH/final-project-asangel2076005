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

        # If no keys and values are provided in the body in POSTMAN
        if not request_data:
            return "No student data added"

        # If you include CLASS_ID in the body
        if "CLASS_ID" in request_data.keys():
            return "Cannot enter a class ID"

        allowed_keys = ["CLASS_CAPACITY", "CLASS_NAME", "FACILITY_ID"]
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

        try:
            class_capacity = int(request_data["CLASS_CAPACITY"])
            class_name = request_data["CLASS_NAME"]
            facility_id = int(request_data["FACILITY_ID"])
        except ValueError:
            return "CLASS CAPACITY and FACILITY ID must be integer"

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
        request_data = request.get_json()

        # Check if the student exists
        sql = f"SELECT * FROM CLASSROOM WHERE CLASS_ID = {class_id};"
        # Check will return ONE dictionary INSIDE a list
        # If you want to access the values inside the dictionary,
        # you must enter check[0]["STUDENT_ID"] to retrieve the number
        check = execute_read_query(connection, sql)
        if not check:
            return "Classroom does not exist"

        # If STUDENT_ID is part of the body in POSTMAN, error will occur
        if "CLASS_ID" in request_data.keys():
            return "Cannot modify classroom ID"

        allowed_keys = ["CLASS_CAPACITY", "CLASS_NAME", "FACILITY_ID"]
        retrieved_keys = [key for key in request_data.keys()]

        # If you put a key other than what's in allowed_keys such as JOB_CODE OR EMPLOYEE_CODE, then an error will show
        for key in retrieved_keys:
            if key not in allowed_keys:
                return f"Invalid key(s) not allowed\n" \
                       f"Keys must be: {', '.join(allowed_keys)}"

        sets = []

        if "CLASS_CAPACITY" in request_data.keys():
            try:
                class_capacity = int(request_data["CLASS_CAPACITY"])
            except ValueError:
                return "CLASS CAPACITY must be INTEGER"
            sets.append({"CLASS_CAPACITY": class_capacity})

        if "CLASS_NAME" in request_data.keys():
            class_name = str(request_data["CLASS_NAME"])
            sets.append({"CLASS_NAME": class_name})

        if "FACILITY_ID" in request_data.keys():
            try:
                facility_id = int(request_data["FACILITY_ID"])
            except ValueError:
                return "FACILITY ID must be INTEGER"

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
