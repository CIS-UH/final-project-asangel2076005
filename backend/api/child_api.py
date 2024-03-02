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

    # Retrieve all child entity instances from the database
    @app.route("/api/child", methods=["GET"])
    def retrieve_child():
        sql = "SELECT * FROM CHILD;"
        child = execute_read_query(connection, sql)
        return jsonify(child)

    # Retrieve a child instance by ID
    @app.route("/api/child/<int:child_id>", methods=["GET"])
    def retrieve_child_id(child_id):
        sql = "SELECT * FROM CHILD;"
        child = execute_read_query(connection, sql)

        for entity in child:
            if entity["CHILD_ID"] == child_id:
                return jsonify(entity)
        return "Invalid ID"

    # Delete a child instance
    @app.route("/api/child/<int:child_id>", methods=["DELETE"])
    def delete_child_id(child_id):
        sql = "SELECT * FROM CHILD;"
        child = execute_read_query(connection, sql)

        for i in range(len(child) - 1, -1, -1):  # start, stop, step size
            id_to_delete = child[i]["CHILD_ID"]
            if child_id == id_to_delete:
                first_name = child[i]["CHILD_FNAME"]
                last_name = child[i]["CHILD_LNAME"]
                delete_statement = f"Successfully deleted {first_name} {last_name} from the database"
                delete_query = f"DELETE FROM CHILD WHERE CHILD_ID = {child_id}"
                delete_sql = execute_query(connection, delete_query)
                return delete_statement, delete_sql

        return "Invalid ID"

    # Add a child entity
    @app.route("/api/child", methods=["POST"])
    def add_child():
        request_data = request.get_json()

        # If no keys and values are provided in the body in POSTMAN
        if not request_data:
            return "No child data added"

        # If you include CHILD_ID in the body
        if "CHILD_ID" in request_data.keys():
            return "Cannot enter a child ID"

        allowed_keys = ["CHILD_FNAME", "CHILD_LNAME", "CHILD_AGE", "CLASS_ID"]
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
            first_name = str(request_data["CHILD_FNAME"])
            last_name = str(request_data["CHILD_LNAME"])
            age = int(request_data["CHILD_AGE"])
            class_id = int(request_data["CLASS_ID"])
        except ValueError:
            return f"AGE and CLASS ID must be integer"
        # Keeps this query for now but does not execute it.
        add_query = f"INSERT INTO CHILD (CHILD_FNAME, CHILD_LNAME, CHILD_AGE, CLASS_ID) " \
                    f"VALUES ('{first_name}', '{last_name}', {age}, {class_id});"

        # Lists the allowed classrooms by ID and continues only if the provided class_id matches any allowed classrooms
        sql = f"SELECT * FROM CLASSROOM"
        classroom = execute_read_query(connection, sql)
        allowed_classrooms = [classroom[i]["CLASS_ID"] for i in range(len(classroom))]
        if class_id not in allowed_classrooms:
            return "Invalid classroom"

        # Counts the number of students in the provided classroom
        sql = f"SELECT COUNT(*) as num_children FROM CHILD WHERE CLASS_ID = {class_id};"
        num_students = execute_read_query(connection, sql)[0]["num_children"]

        # Counts the number of teachers in the provided classroom
        sql = f"SELECT COUNT(*) as num_teacher FROM TEACHER WHERE CLASS_ID = {class_id};"
        num_teacher = execute_read_query(connection, sql)[0]["num_teacher"]

        for room in classroom:
            if room["CLASS_ID"] == class_id:
                if num_students >= room["CLASS_CAPACITY"]:
                    return "Cannot add more students. Room is full or number of students have exceeded the capacity"

                # Bounds to a variable whether a child can be added to the room or not
                if num_students < 10 * num_teacher:
                    insertion_status = True
                else:
                    insertion_status = False

                if not insertion_status:
                    return "Cannot add student. Number of teachers most likely cannot guide more students"
                else:
                    execute_query(connection, add_query)
                    return f"Child addition success"


    # Update a child entity
    @app.route("/api/child/<int:child_id>", methods=["PUT"])
    def update_child_id(child_id):
        request_data = request.get_json()

        sql = f"SELECT * FROM CHILD WHERE CHILD_ID = {child_id};"
        check = execute_read_query(connection, sql)
        if not check:
            return "Child does not exist"

        if "CHILD_ID" in request_data.keys():
            return "Cannot modify child ID"

        allowed_keys = ["CHILD_FNAME", "CHILD_LNAME", "CHILD_AGE", "CLASS_ID"]
        retrieved_keys = [key for key in request_data.keys()]

        # If you put a key other than what's in allowed_keys such as JOB_CODE OR EMPLOYEE_CODE, then an error will show
        for key in retrieved_keys:
            if key not in allowed_keys:
                return f"Invalid key(s) not allowed\n" \
                       f"Keys must be: {', '.join(allowed_keys)}"

        sets = []

        if "CHILD_FNAME" in request_data.keys():
            first_name = str(request_data["CHILD_FNAME"])
            sets.append({"CHILD_FNAME": first_name})

        if "CHILD_LNAME" in request_data.keys():
            last_name = str(request_data["CHILD_LNAME"])
            sets.append({"CHILD_LNAME": last_name})

        if "CHILD_AGE" in request_data.keys():
            try:
                age = int(request_data["CHILD_AGE"])
            except ValueError:
                return "AGE must be integer"
            sets.append({"CHILD_AGE": age})

        if "CLASS_ID" in request_data.keys():
            try:
                class_id = int(request_data["CLASS_ID"])
            except ValueError:
                return "CLASS ID must be integer"

            # Lists the allowed classrooms by ID and continues
            # only if the provided class_id matches any allowed classrooms
            sql = f"SELECT * FROM CLASSROOM"
            classroom = execute_read_query(connection, sql)
            allowed_classrooms = [classroom[i]["CLASS_ID"] for i in range(len(classroom))]
            if class_id not in allowed_classrooms:
                return "Invalid classroom"

            # Counts the number of students in the provided classroom
            sql = f"SELECT COUNT(*) as num_children FROM CHILD WHERE CLASS_ID = {class_id};"
            num_students = execute_read_query(connection, sql)[0]["num_children"]

            # Counts the number of teachers in the provided classroom
            sql = f"SELECT COUNT(*) as num_teacher FROM TEACHER WHERE CLASS_ID = {class_id};"
            num_teacher = execute_read_query(connection, sql)[0]["num_teacher"]

            for room in classroom:
                if room["CLASS_ID"] == class_id:
                    if num_students >= room["CLASS_CAPACITY"]:
                        return "Cannot add more students. Room is full"

                    # Bounds to a variable whether a child can be added to the room or not
                    if num_students < 10 * num_teacher:
                        insertion_status = True
                    else:
                        insertion_status = False

                    if not insertion_status:
                        return "Cannot add student. Number of teachers most likely cannot guide more students"
                    else:
                        sets.append({"CLASS_ID": class_id})

        for item in sets:
            for key, value in item.items():
                if isinstance(value, int):
                    update_sql = f"UPDATE CHILD SET {key} = {value} WHERE CHILD_ID = {child_id};"
                else:
                    update_sql = f"UPDATE CHILD SET {key} = '{value}' WHERE CHILD_ID = {child_id};"
                execute_query(connection, update_sql)

        return "Update success"
    app.run()
