import os
from flask import Flask
import subprocess

app = Flask(__name__)

@app.route("/")
def replicator():
    proc = subprocess.Popen(["gsutil", "-m", "rsync", "-d", "-r", "gs://masood-mumbai", "gs://masood-delhi"])
    try:
        outs, errs = proc.communicate(timeout=60)
    except subprocess.TimeoutExpired:
        proc.kill()
        outs, errs = proc.communicate()
    print(outs)
    return "1"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))