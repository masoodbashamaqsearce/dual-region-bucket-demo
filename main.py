import os
from flask import Flask, request
import subprocess
import base64
import logging as log
import google.cloud.logging as logging

app = Flask(__name__)

@app.route("/", methods=['POST'])
def replicator():
    logging_client = logging.Client()
    logging_client.setup_logging()
    data = request.get_json()
    request.ack()
    if not data:
        msg = 'no Pub/Sub message received'
        print(f'error: {msg}')
        return f'Bad Request: {msg}', 400

    if not isinstance(data, dict) or 'message' not in data:
        msg = 'invalid Pub/Sub message format'
        print(f'error: {msg}')
        return f'Bad Request: {msg}', 400

    log.info(data)
    pubsub_message = data['message']
    name = 'World'
    if isinstance(pubsub_message, dict) and 'data' in pubsub_message:
        name = base64.b64decode(pubsub_message['data']).decode('utf-8').strip()
        
    resp = f"Hello, {name}! ID: {request.headers.get('ce-id')}"
    log.info(resp)
    log.info(data.keys())
    return (resp, 200)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
