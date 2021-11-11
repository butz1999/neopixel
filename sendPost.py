import requests

requests.post("http://localhost:8080/image/data", data=bytes("Hallo Welt!", "utf-8"))
