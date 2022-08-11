import requests
import sys
import epiCalendar

# Verifies if the cookie is valid server-side.
# This check is slower than the basic cookie verification, but it is 100% reliable.
def verifyCookieExpiration(cookie) -> bool:
    payload = {
        'JSESSIONID': cookie,
        'cookieconsent_status': 'dismiss'
    }
    r = requests.get(epiCalendar.url, cookies=payload)
    if '<div id="j_id' in r.text:
            return True
    return False

# Quick cookie verification.
# Checks if the structure of the cookie matches '0000XXXXXXXXXXXXXXXXXXXXXXX:1dXXXXXXX'.
def verifyCookieStructure(cookie) -> bool:
    if cookie is None: return False
    if cookie == "0000XXXXXXXXXXXXXXXXXXXXXXX:1dXXXXXXX": return False
    if len(cookie) != 37: return False
    for i in range(4):
        if cookie[i] != "0": return False
    if cookie[27] != ":" or cookie[28] != "1" or cookie[29] != "d":
        return False
    return True

if __name__ == "__main__":
    try:
        result = verifyCookieExpiration(sys.argv[1])
        print(result)
        exit(0 if result == True else 1)
    except Exception:
        print("Usage: python3 fastCheckCookieExpiration.py <cookie>")
        exit(2)