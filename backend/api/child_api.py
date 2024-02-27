import flask
from flask import jsonify, request
from self_made_modules.sql_helper import create_connection, execute_read_query, execute_query
from self_made_modules import creds

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

    app.run()
