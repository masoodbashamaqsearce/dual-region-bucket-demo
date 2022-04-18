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
    #log.info(wholedata)
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
    sp = subprocess.Popen(["gsutil","label","get",source],stdout=subprocess.PIPE)
    out = sp.stdout.read()
    if len(out) > 0:
        log.info(type(out))
        log.info(out)
        dr_flg = json.loads(str(out,"utf-8"))
        if "dual-region" in dr_flg.keys():
            if dr_flg["dual-region"] != "true":
                log.info("bucket is not dual region, event skipped")
                return ("ok",203)
        else:
            log.info("bucket is not dual region, event skipped")
            return ("ok",205)
    else:
        log.info("bucket is not dual region, event skipped")
        return ("ok",206)
    if obj_name[-1] == '/':
        log.info("folder created..., event skipped")
        return('ok',204)
    source = "gs://" + scr_bucket + "/" + obj_name
    dest_bucket = scr_bucket + "-delhi-backup/"
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

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
