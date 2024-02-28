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
                first_name = teacher[i]["TEACHER_FNAME"]
                last_name = teacher[i]["TEACHER_LNAME"]
                delete_statement = f"Successfully deleted {first_name} {last_name} from the database"
                delete_query = f"DELETE FROM TEACHER WHERE TEACHER_ID = {teacher_id}"
                delete_sql = execute_query(connection, delete_query)
                return delete_statement, delete_sql

        return "Invalid ID"

    # Add a teacher entity
    @app.route("/api/teacher", methods=["POST"])
    def add_teacher():
        request_data = request.get_json()

        if (not request_data) or ("TEACHER_ID" in request_data.keys()):
            return "No teacher details provided"

        columns = [key for key in request_data.keys()]

        if (len(columns) > 3) or (len(columns) < 3):
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
        # Check if the teacher exists in the database
        sql = f"SELECT * FROM TEACHER WHERE TEACHER_ID = {teacher_id};"
        check = execute_read_query(connection, sql)

        if not check:
            return "Teacher with the provided ID does not exist"

        request_data = request.get_json()

        sets = []

        if "TEACHER_FNAME" in request_data.keys():
            first_name = request_data["TEACHER_FNAME"]
            sets.append({"TEACHER_FNAME": first_name})

        if "TEACHER_LNAME" in request_data.keys():
            last_name = request_data["TEACHER_LNAME"]
            sets.append({"TEACHER_LNAME": last_name})

        if "CLASS_ID" in request_data.keys():
            class_id = request_data["CLASS_ID"]

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

    app.run()
