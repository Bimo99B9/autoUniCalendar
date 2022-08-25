import requests

url = 'https://sies.uniovi.es/serviciosacademicos/web/expedientes/calendario.xhtml'

def firstRequest(jsessionid) -> requests.Response:
    return requests.get(url, cookies={'JSESSIONID': jsessionid})

def postRequest(payload, jsessionid) -> requests.Response:
    return requests.post(url, data=payload, headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}, cookies={'JSESSIONID': jsessionid})