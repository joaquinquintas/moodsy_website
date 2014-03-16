import requests

payload = {'email': 'hugo@osvaldobarrera.com.ar'}

r = requests.post("http://localhost:7555/subscribers/signup", data=payload)
print(r.status_code)
