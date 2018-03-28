from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import sys
import os

app = Flask(__name__)
CORS(app)
urls = {}

@app.route('/chat')
def main():
    # List our bots... in a production system this wouldn't be static, but passed via file
    bots = ["agent007"]
    baseUrl = "http://||agent||:4000/post_message"
    # If a file had been passed like in a production system, it might look like this:
    #with open("agents.txt", "r") as AgentFile:
    #    for line in AgentFile.read().splitlines():
    #        urls[line] = baseUrl.replace("||agent||", line)
    for bot in bots:
        urls[bot] = baseUrl.replace("||agent||", bot)

    sender = request.args.get('sender')
    bot = request.args.get('context')
    message = request.args.get('message')

    if bot != None and message != None and sender != None:
        if bot in urls:
            response = requests.post(urls[bot], 
                                 json = {"sender" : sender, "message" : message},
                                 headers = {"Content-Type" : "application/json"})
            return jsonify(response.json())
        else:
            return jsonify("The " + bot + " chatbot provided in the context does not exist")
    elif bot == None:
        return jsonify("You must provide a context parameter")
    elif message == None:
        return jsonify("You must provide a message parameter")
    elif sender == None:
        return jsonify("You must provide a sender parameter")

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')