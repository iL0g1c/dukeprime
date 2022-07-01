import flask
from flask import request, jsonify
import jsonlines

app = flask.Flask(__name__)
file_path = "/var/www/backend/database/"
@app.route("/api/servers/all", methods=["GET"])
def all_servers():
    guilds = []
    with jsonlines.open(f"{file_path}guilds.jl", "r") as reader:
        for obj in reader:
            guilds.append(obj)
    reader.close()
    return jsonify(guilds)
    
@app.route("/api/servers", methods=["GET"])
def server_by_id():
    if "id" in request.args:
        id = int(request.args["id"])
    else:
        return "Error: No id field provided."
    
    with jsonlines.open(f"{file_path}guilds.jl", "r") as reader:
        for obj in reader:
            if obj["id"] == id:
                return obj

@app.route("/api/servers/users/all", methods=["GET"])
def all_server_users():
    if "server_id" in request.args:
        server_id = int(request.args["server_id"])
    else:
        return "Error: No server_id field provided."
    
    users = []
    with jsonlines.open(f"{file_path}{server_id}.jl", "r") as reader:
        for obj in reader:
            users.append(obj)
    return jsonify(users)

@app.route("/api/servers/users", methods=["GET"])
def get_user():
    if "server_id" in request.args:
        if "user_id" in request.args:
            server_id = int(request.args["server_id"])
            user_id = int(request.args["user_id"])
        else:
            return "Error: No user_id field provided."
    else:
        return "Error: No server_id field provided."
    
    with jsonlines.open(f"{file_path}{server_id}.jl", "r") as reader:
        for obj in reader:
            if obj["user"] == user_id:
                return obj

@app.route("/api/users")
def search_user():
    if "id" in request.args:
        id = int(request.args["id"])
    else:
        return "Error: No id field provided."
    
    with jsonlines.open(f"{file_path}guilds.jl", "r") as reader_one:
        for obj in reader_one:
            with jsonlines.open(f"{file_path}{obj['file']}") as reader_two:
                for item in reader_two:
                    if item["user"] == id:
                        return {"user_data": item, "server": obj["id"]}


if __name__ == "__main__":
    app.run()
