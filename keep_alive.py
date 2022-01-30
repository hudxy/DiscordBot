from flask import Flask
from threading import Thread

app = Flask(__name__)


@app.route('/')
def alive():
    return "Your bot is alive!"
  
def run():
    app.run(host='0.0.0.0')
		
def keep_alive():
    server = Thread(target=run)
    server.start()