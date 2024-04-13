import flask
from flask import jsonify, request
from flask_cors import CORS
from self_made_modules.sql_helper import create_connection, execute_read_query, execute_query
from self_made_modules import creds
# Ensure flask_cors is installed; otherwise, UX design (find capacity) will not work


if __name__ == "__main__":
    # setting up an application name
    app = flask.Flask(__name__)  # sets up the application
    app.config["DEBUG"] = True  # allow to show errors in browser

    # Disables CORS blocking API calls from this port to webserver Fetch API calls
    CORS(app)

    my_creds = creds.Creds()
    connection = create_connection(my_creds.connection_string,
                                   my_creds.user_name,
                                   my_creds.password,
                                   my_creds.database_name)

    # Default URL without any routing
    @app.route('/', methods=["GET"])
    def home():
        return "<h1><center>Welcome to the School API</center></h1>"

    # Login API
    # username: admin
    # password: password
    @app.route("/api/login", methods=["GET"])
    def user_login():
        username = request.headers["username"]
        password = request.headers["password"]

        if (username == "admin") and (password == "password"):
            return "Login Success"

        return "Login Failed"

    # FACILITY
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
                delete_query = f"DELETE FROM FACILITY WHERE FACILITY_ID = {facility_id}"
                delete_sql = execute_query(connection, delete_query)
                check_sql = f"SELECT * FROM FACILITY WHERE FACILITY_ID = {facility_id}"
                check = execute_read_query(connection, check_sql)
                if check:
                    return "Cannot delete facility: Referenced by other entities in other table"
                delete_statement = f"Facility Delete Success"
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
            facility_name = str(request_data["FACILITY_NAME"].capitalize())
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

        facility_name = request_data["FACILITY_NAME"].capitalize()

        sql = f"UPDATE FACILITY SET FACILITY_NAME = '{facility_name}' WHERE FACILITY_ID = {facility_id}"
        execute_query(connection, sql)

        return "Facility Update Success"

    # CLASSROOM
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
                delete_query = f"DELETE FROM CLASSROOM WHERE CLASS_ID = {class_id}"
                delete_sql = execute_query(connection, delete_query)
                check_sql = f"SELECT * FROM CLASSROOM WHERE CLASS_ID = {class_id}"
                check = execute_read_query(connection, check_sql)
                if check:
                    return "Cannot delete classroom: Referenced by other entities in other table"
                delete_statement = f"Classroom Delete Success"
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
            class_name = request_data["CLASS_NAME"].capitalize()
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

        # Check if the classroom exists
        sql = f"SELECT * FROM CLASSROOM WHERE CLASS_ID = {class_id};"
        check = execute_read_query(connection, sql)
        if not check:
            return "Classroom does not exist"

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
            class_name = str(request_data["CLASS_NAME"].capitalize())
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

        return "Classroom Update success"

    # TEACHER
    # Retrieve all teacher entity instances from the database
    @app.route("/api/teacher", methods=["GET"])
    def retrieve_teacher():
        sql = "SELECT * FROM TEACHER;"
        teacher = execute_read_query(connection, sql)
        return jsonify(teacher)

    # Retrieve a teacher instance by ID
    @app.route("/api/teacher/<int:teacher_id>", methods=["GET"])
    def retrieve_teacher_id(teacher_id):
        sql = "SELECT * FROM TEACHER;"
        teacher = execute_read_query(connection, sql)

        for entity in teacher:
            if entity["TEACHER_ID"] == teacher_id:
                return jsonify(entity)
        return "Invalid ID"

    # Delete a teacher instance
    @app.route("/api/teacher/<int:teacher_id>", methods=["DELETE"])
    def delete_teacher_id(teacher_id):
        sql = "SELECT * FROM TEACHER;"
        teacher = execute_read_query(connection, sql)

        for i in range(len(teacher) - 1, -1, -1):  # start, stop, step size
            id_to_delete = teacher[i]["TEACHER_ID"]
            if teacher_id == id_to_delete:
                delete_query = f"DELETE FROM TEACHER WHERE TEACHER_ID = {teacher_id}"
                delete_sql = execute_query(connection, delete_query)
                check_sql = f"SELECT * FROM TEACHER WHERE TEACHER_ID = {teacher_id}"
                check = execute_read_query(connection, check_sql)
                if check:
                    return "Cannot delete Teacher: Referenced by other entities in other table"
                delete_statement = f"Delete Teacher Success"
                return delete_statement, delete_sql

        return "Invalid ID"

    # Add a teacher entity
    @app.route("/api/teacher", methods=["POST"])
    def add_teacher():
        request_data = request.get_json()

        # If no keys and values are provided in the body in POSTMAN
        if not request_data:
            return "No teacher data added"

        # If you include TEACHER_ID in the body
        if "TEACHER_ID" in request_data.keys():
            return "Cannot enter a teacher ID"

        allowed_keys = ["TEACHER_FNAME", "TEACHER_LNAME", "CLASS_ID"]
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
            first_name = str(request_data["TEACHER_FNAME"].capitalize())
            last_name = str(request_data["TEACHER_LNAME"].capitalize())
            class_id = int(request_data["CLASS_ID"])
        except ValueError:
            return "CLASS ID must be integer"

        # Keeps this query for now but does not execute it.
        add_query = f"INSERT INTO TEACHER (TEACHER_FNAME, TEACHER_LNAME, CLASS_ID) " \
                    f"VALUES ('{first_name}', '{last_name}', {class_id});"

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

        # For circumstances where a classroom has no students but has a capacity
        if (num_students == 0) and (num_teacher == 0):
            execute_query(connection, add_query)
            return "Teacher addition success"

        for room in classroom:
            if room["CLASS_ID"] == class_id:
                # Calculates the amount of teachers needed according to the capacity of the room
                teachers_needed = room["CLASS_CAPACITY"] // 10
                # If there's a remainder, an additional teacher is needed to accommodate the capacity of students
                if room["CLASS_CAPACITY"] % 10 != 0:
                    teachers_needed += 1
                if num_students > room["CLASS_CAPACITY"]:
                    return "Error: Number of students exceed room capacity. Cannot assign teachers"

                if num_teacher >= teachers_needed:
                    return "Addition Failed: Too many teachers"
                else:
                    execute_query(connection, add_query)
                    return "Teacher addition success"

    # Update a teacher entity
    @app.route("/api/teacher/<int:teacher_id>", methods=["PUT"])
    def update_teacher_id(teacher_id):
        request_data = request.get_json()

        # Check if the teacher exists
        sql = f"SELECT * FROM TEACHER WHERE TEACHER_ID = {teacher_id};"
        check = execute_read_query(connection, sql)
        if not check:
            return "Teacher does not exist"

        if "TEACHER_ID" in request_data.keys():
            return "Cannot modify teacher ID"

        allowed_keys = ["TEACHER_FNAME", "TEACHER_LNAME", "CLASS_ID"]
        retrieved_keys = [key for key in request_data.keys()]

        # If you put a key other than what's in allowed_keys such as JOB_CODE OR EMPLOYEE_CODE, then an error will show
        for key in retrieved_keys:
            if key not in allowed_keys:
                return f"Invalid key(s) not allowed\n" \
                       f"Keys must be: {', '.join(allowed_keys)}"

        sets = []

        if "TEACHER_FNAME" in request_data.keys():
            first_name = str(request_data["TEACHER_FNAME"].capitalize())
            sets.append({"TEACHER_FNAME": first_name})

        if "TEACHER_LNAME" in request_data.keys():
            last_name = str(request_data["TEACHER_LNAME"].capitalize())
            sets.append({"TEACHER_LNAME": last_name})

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

            # For circumstances where a classroom has no students but has a capacity
            if (num_students == 0) and (num_teacher == 0):
                sets.append({"CLASS_ID": class_id})

            for room in classroom:
                if room["CLASS_ID"] == class_id:
                    # Calculates the amount of teachers needed according to the capacity of the room
                    teachers_needed = room["CLASS_CAPACITY"] // 10
                    # If there's a remainder, an additional teacher is needed to accommodate the capacity of students
                    if room["CLASS_CAPACITY"] % 10 != 0:
                        teachers_needed += 1
                    if num_students > room["CLASS_CAPACITY"]:
                        return "Error: Number of students exceed room capacity. Cannot assign teachers"

                    if num_teacher >= teachers_needed:
                        return "Addition Failed: Too many teachers"
                    else:
                        sets.append({"CLASS_ID": class_id})

        for item in sets:
            for key, value in item.items():
                if isinstance(value, int):
                    update_sql = f"UPDATE TEACHER SET {key} = {value} WHERE TEACHER_ID = {teacher_id};"
                else:
                    update_sql = f"UPDATE TEACHER SET {key} = '{value}' WHERE TEACHER_ID = {teacher_id};"
                execute_query(connection, update_sql)

        return "Update success"

    # CHILD
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
                delete_query = f"DELETE FROM CHILD WHERE CHILD_ID = {child_id}"
                delete_sql = execute_query(connection, delete_query)
                check_sql = f"SELECT * FROM CHILD WHERE CHILD_ID = {child_id}"
                check = execute_read_query(connection, check_sql)
                if check:
                    return "Cannot delete Child: Referenced by other entities in other table"
                delete_statement = "Delete Child Success"
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
            first_name = str(request_data["CHILD_FNAME"].capitalize())
            last_name = str(request_data["CHILD_LNAME"].capitalize())
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
            first_name = str(request_data["CHILD_FNAME"].capitalize())
            sets.append({"CHILD_FNAME": first_name})

        if "CHILD_LNAME" in request_data.keys():
            last_name = str(request_data["CHILD_LNAME"].capitalize())
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

    # Extra API Calls
    # Child Webpage Functionality: Find seats remaining for user information
    # Will not include rooms that are newly added (meaning no child yet)
    @app.route("/api/capacity", methods=["GET"])
    def retrieve_capacity():
        sql = """SELECT C.CLASS_ID, CLASS_NAME, FACILITY_ID, CLASS_CAPACITY, COUNT(CHILD_ID) AS CHILD_AMT, 
                    (CLASS_CAPACITY - COUNT(CHILD_ID)) AS SEATS_REMAINING
                    FROM CLASSROOM C
                    JOIN CHILD CH ON C.CLASS_ID = CH.CLASS_ID
                    GROUP BY C.CLASS_ID
                    ORDER BY C.CLASS_ID;"""
        capacity = execute_read_query(connection, sql)

        return jsonify(capacity)

    # Teacher Webpage Functionality: Find teacher spaces remaining for user information
    # Will not include rooms that are newly added (meaning no teachers yet)
    @app.route("/api/space", methods=["GET"])
    def retrieve_space():
        sql = """SELECT C.CLASS_ID, CLASS_NAME, FACILITY_ID, CEIL(CLASS_CAPACITY / 10) AS ROUNDED_CAPACITY, 
                COUNT(TEACHER_ID) AS TEACHER_AMT, (CEIL(CLASS_CAPACITY / 10) - COUNT(TEACHER_ID)) AS SPACE_REMAINING
                FROM CLASSROOM C
                JOIN TEACHER T ON C.CLASS_ID = T.CLASS_ID
                GROUP BY C.CLASS_ID
                ORDER BY C.CLASS_ID;"""
        space = execute_read_query(connection, sql)

        return jsonify(space)

    app.run(threaded=True)
