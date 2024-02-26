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
        sql = "SELECT * FROM CLASSROOM ORDER BY CLASS_CAPACITY;"
        classroom = execute_read_query(connection, sql)
        return jsonify(classroom)

    # Retrieve all teacher entity instances from the database
    @app.route("/api/teacher", methods=["GET"])
    def retrieve_teacher():
        sql = "SELECT * FROM TEACHER ORDER BY TEACHER_LNAME, TEACHER_FNAME;"
        teacher = execute_read_query(connection, sql)
        return jsonify(teacher)

    # Retrieve all child entity instances from the database
    @app.route("/api/child", methods=["GET"])
    def retrieve_child():
        sql = "SELECT * FROM CHILD ORDER BY CHILD_FNAME, CHILD_LNAME;"
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
        sql = "SELECT * FROM CLASSROOM ORDER BY CLASS_CAPACITY;"
        classroom = execute_read_query(connection, sql)

        for entity in classroom:
            if entity["CLASS_ID"] == class_id:
                return jsonify(entity)
        return "Invalid ID"

    # Retrieve a teacher instance by ID
    @app.route("/api/teacher/<int:teacher_id>", methods=["GET"])
    def retrieve_teacher_id(teacher_id):
        sql = "SELECT * FROM TEACHER ORDER BY TEACHER_LNAME, TEACHER_FNAME;"
        teacher = execute_read_query(connection, sql)

        for entity in teacher:
            if entity["TEACHER_ID"] == teacher_id:
                return jsonify(entity)
        return "Invalid ID"

    # Retrieve a child instance by ID
    @app.route("/api/child/<int:child_id>", methods=["GET"])
    def retrieve_child_id(child_id):
        sql = "SELECT * FROM CHILD ORDER BY CHILD_FNAME, CHILD_LNAME;"
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

    app.run()
