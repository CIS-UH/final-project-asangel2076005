import flask
from flask import jsonify, request
from sql_helper import create_connection, execute_read_query, execute_query
import creds
from math import ceil

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

    # This section is for retrieving all objects from each entity
    # Retrieve all facility entity instances from the database
    @app.route("/api/facility", methods=["GET"])
    def retrieve_facility():
        sql = "SELECT * FROM FACILITY;"
        facility = execute_read_query(connection, sql)
        return jsonify(facility)

    # Retrieve all classroom entity instances from the database
    @app.route("/api/classroom", methods=["GET"])
    def retrieve_classroom():
        sql = "SELECT * FROM CLASSROOM;"
        classroom = execute_read_query(connection, sql)
        return jsonify(classroom)

    # Retrieve all teacher entity instances from the database
    @app.route("/api/teacher", methods=["GET"])
    def retrieve_teacher():
        sql = "SELECT * FROM TEACHER;"
        teacher = execute_read_query(connection, sql)
        return jsonify(teacher)

    # Retrieve all child entity instances from the database
    @app.route("/api/child", methods=["GET"])
    def retrieve_child():
        sql = "SELECT * FROM CHILD;"
        child = execute_read_query(connection, sql)
        return jsonify(child)

    # This section is for retrieving an entity instance from each entity
    # Retrieve a facility instance by ID
    @app.route("/api/facility/<int:facility_id>", methods=["GET"])
    def retrieve_facility_id(facility_id):
        sql = "SELECT * FROM FACILITY"
        facility = execute_read_query(connection, sql)

        for entity in facility:
            if entity["FACILITY_ID"] == facility_id:
                return jsonify(entity)
        return "Invalid ID"

    # Retrieve a classroom instance by ID
    @app.route("/api/classroom/<int:class_id>", methods=["GET"])
    def retrieve_classroom_id(class_id):
        sql = "SELECT * FROM CLASSROOM;"
        classroom = execute_read_query(connection, sql)

        for entity in classroom:
            if entity["CLASS_ID"] == class_id:
                return jsonify(entity)
        return "Invalid ID"

    # Retrieve a teacher instance by ID
    @app.route("/api/teacher/<int:teacher_id>", methods=["GET"])
    def retrieve_teacher_id(teacher_id):
        sql = "SELECT * FROM TEACHER;"
        teacher = execute_read_query(connection, sql)

        for entity in teacher:
            if entity["TEACHER_ID"] == teacher_id:
                return jsonify(entity)
        return "Invalid ID"

    # Retrieve a child instance by ID
    @app.route("/api/child/<int:child_id>", methods=["GET"])
    def retrieve_child_id(child_id):
        sql = "SELECT * FROM CHILD;"
        child = execute_read_query(connection, sql)

        for entity in child:
            if entity["CHILD_ID"] == child_id:
                return jsonify(entity)
        return "Invalid ID"

    # This section involves the deletion of an entity instance from each table
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

    # Delete a teacher instance
    @app.route("/api/teacher/<int:teacher_id>", methods=["DELETE"])
    def delete_teacher_id(teacher_id):
        sql = "SELECT * FROM TEACHER;"
        teacher = execute_read_query(connection, sql)

        for i in range(len(teacher) - 1, -1, -1):  # start, stop, step size
            id_to_delete = teacher[i]["TEACHER_ID"]
            if teacher_id == id_to_delete:
                first_name = teacher[i]["TEACHER_FNAME"]
                last_name = teacher[i]["TEACHER_LNAME"]
                delete_statement = f"Successfully deleted {first_name} {last_name} from the database"
                delete_query = f"DELETE FROM TEACHER WHERE TEACHER_ID = {teacher_id}"
                delete_sql = execute_query(connection, delete_query)
                return delete_statement, delete_sql

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

    # This section goes over adding an entity instance to each table
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

    # Add a classroom entity
    @app.route("/api/classroom", methods=["POST"])
    def add_classroom():
        request_data = request.get_json()

        if not request_data:
            return "No classroom details provided"

        if ("CLASS_CAPACITY" and "CLASS_NAME" and "FACILITY_ID") not in request_data.keys():
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

    # Add a teacher entity
    @app.route("/api/teacher", methods=["POST"])
    def add_teacher():
        request_data = request.get_json()

        if not request_data:
            return "No teacher details provided"

        if ("TEACHER_FNAME" and "TEACHER_LNAME" and "CLASS_ID") not in request_data.keys():
            return "Incomplete data, try again"

        first_name = request_data["TEACHER_FNAME"]
        last_name = request_data["TEACHER_LNAME"]
        class_id = request_data["CLASS_ID"]
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
            return "Addition Success"

        for room in classroom:
            if room["CLASS_ID"] == class_id:
                # Calculates the amount of teachers needed according to the capacity of the room
                teachers_needed = ceil(room["CLASS_CAPACITY"] // 10)
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

    # This section involves updating an entity instance for each table
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
