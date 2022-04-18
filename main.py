import os,json
from flask import Flask, request
import subprocess
import base64
import logging as log
import google.cloud.logging as logging

app = Flask(__name__)

@app.route("/create", methods=['POST'])
def create():
    logging_client = logging.Client()
    logging_client.setup_logging()
    data = request.get_json()
    log.info("create method called")
    wholedata = f"wholedata : {data} ::end of data"
    log.info(wholedata)
    prt = "data['protoPayload']['methodName']:"+data['protoPayload']['methodName']
    log.info(prt)
    prt = "data['protoPayload']['resourceName']:"+data['protoPayload']['resourceName']
    log.info(prt)
    prt = "data['resource']['labels']['bucket_name']:"+data['resource']['labels']['bucket_name']
    log.info(prt)
    prt = "data['resource']['labels']['location']:"+data['resource']['labels']['location']
    log.info(prt)
    scr_bucket = data['resource']['labels']['bucket_name']
    obj_name = data['protoPayload']['resourceName'].split("/objects/")[1]
    source = "gs://" + scr_bucket
    subprocess.Popen(["gsutil","label","get",source])
    outs, errs = proc.communicate()
    log.info(outs)
    if obj_name[-1] == '/':
        log.info("folder created...")
        log.info("event skipped")
        return('ok',204)
    source = "gs://" + scr_bucket + obj_name
    dest_bucket = scr_bucket + "-delhi-backup"
    dest = "gs://" + dest_bucket + obj_name
    proc = subprocess.Popen(["gsutil", "-m", "cp", "-r", "-p", source, dest])
    try:
        outs, errs = proc.communicate()
        log.info('OK')
        return ('OK', 200)
    except Exception as e:
        log.info(e)
        proc.kill()
        outs, errs = proc.communicate()
        log.info('NOT OK')
        return ('NOT OK', 402)
    


@app.route("/update", methods=['POST'])
def update():
    logging_client = logging.Client()
    logging_client.setup_logging()
    data = request.get_json()
    log.info("root method called...")
    wholedata = f"wholedata : {data} ::end of data"
    log.info(wholedata)
    prt = "data['protoPayload']['methodName']:"+data['protoPayload']['methodName']
    log.info(prt)
    prt = "data['protoPayload']['resourceName']:"+data['protoPayload']['resourceName']
    log.info(prt)
    prt = "data['resource']['labels']['bucket_name']:"+data['resource']['labels']['bucket_name']
    log.info(prt)
    prt = "data['resource']['labels']['location']:"+data['resource']['labels']['location']
    log.info(prt)
    return ('OK', 200)

@app.route("/", methods=['POST'])
def main():
    logging_client = logging.Client()
    logging_client.setup_logging()
    data = request.get_json()
    log.info("root method called...")
    wholedata = f"wholedata : {data} ::end of data"
    log.info(wholedata)
    prt = "data['protoPayload']['methodName']:"+data['protoPayload']['methodName']
    log.info(prt)
    prt = "data['protoPayload']['resourceName']:"+data['protoPayload']['resourceName']
    log.info(prt)
    prt = "data['resource']['labels']['bucket_name']:"+data['resource']['labels']['bucket_name']
    log.info(prt)
    prt = "data['resource']['labels']['location']:"+data['resource']['labels']['location']
    log.info(prt)
    return ('OK', 200)

@app.route("/delete", methods=['POST'])
def delete():
    logging_client = logging.Client()
    logging_client.setup_logging()
    data = request.get_json()
    pubsub_message = data['message']
    log.info("delete method called...")
    name = 'World'
    if isinstance(pubsub_message, dict) and 'data' in pubsub_message:
        name = base64.b64decode(pubsub_message['data']).decode('utf-8').strip()
        
    resp = f"Hello, {name}! ID: {request.headers.get('ce-id')}"
    log.info(name)
    return (resp, 200)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
