from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import jsonlines as jl
import ast

app = Flask(__name__)
api = Api(app)
file_path = "/var/www/backend/database/"
def get_guild(guild_id):
    with jl.open(file_path + "guilds.jl", "r") as reader:
        for obj in reader:
            if obj["id"] == guild_id:
                data = obj
                break
    reader.close()
    return guild_id

def get_user(user_id, guild_id):
    guild = []
    with jl.open(f"{file_path}{guild_id}.jl", "r") as reader:
        for obj in reader:
            guild.append(obj)
    reader.close()
    for user in guild:
        if user["user"] == user_id:
            return user

class Servers(Resource):
    def get(self):
        server_id = request.args.get("server_id")
        data = get_guild(int(server_id))
        return {"data": data}, 200

class Users(Resource):
    def get(self):
        server_id = request.args.get("server_id")
        user_id = request.args.get("user_id")
        guild_id = get_guild(int(server_id))
        data = get_user(int(user_id), guild_id)
        return {"data": data}, 200

api.add_resource(Servers, '/servers')
api.add_resource(Users, '/users')

if __name__ == '__main__':
    app.run()
