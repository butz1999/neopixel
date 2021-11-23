import requests
import time

while True:
    response = requests.post("http://localhost:8080/test/random/32")
    time.sleep(1)
