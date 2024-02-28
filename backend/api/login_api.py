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

    # Default URL without any routing
    @app.route('/', methods=["GET"])
    def home():
        return "<h1><center>Welcome to the School API</center></h1>"

    # Login API
    # username: asangel
    # password: haha12345
    @app.route("/api/login", methods=["GET"])
    def user_login():
        username = request.headers["username"]
        password = request.headers["password"]

        if (username == "asangel") and (password == "haha12345"):
            return "Login Success"

        return "Login Failed"

    app.run()
