from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def main():
    return 'Bot is Online'

def run():
    app.run(host='0.0.0.0', port=8080)

def begin():
    server = Thread(target=run)
    server.start()
