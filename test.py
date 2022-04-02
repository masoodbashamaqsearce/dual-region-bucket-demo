import subprocess

proc = subprocess.Popen(["gsutil", "-m", "rsync", "-d", "-r", "gs://masood-mumbai", "gs://masood-delhi"])
try:
    outs, errs = proc.communicate(timeout=60)
    # now you can do something with the text in outs and errs
except subprocess.TimeoutExpired:
    proc.kill()
    outs, errs = proc.communicate()

print(outs)
