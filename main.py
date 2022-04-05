import os
from flask import Flask
import subprocess

app = Flask(__name__)

@app.route("/", methods=['POST'])
def replicator(__GCP_CloudEventsMode=None):
    print(__GCP_CloudEventsMode)
    subprocess.Popen(["gsutil", "-m", "rsync", "gs://masood-mumbai/100gb_file", "gs://masood-delhi/"])
    return "1"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
