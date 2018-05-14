import requests
import base64
f = open("ring.jpg", "rb")
string = f.read()
data = base64.encodestring(string)

r = requests.post("http://192.168.2.7:5000/predict", data)

assert r.status_code == 200 and r.reason == "OK"
print(r.status_code, r.reason, r.text)
