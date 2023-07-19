# Function to send the first GET HTTP request using the tokens provided.
import requests


def get_first_request(url, session_token, render_token):
    print("[@] Sending the first request...")

    # Cookies payload of the HTTP request.
    payload = {"JSESSIONID": session_token, "oam.Flash.RENDERMAP.TOKEN": render_token}

    r = requests.get(url, cookies=payload)
    print("[#] First request correctly finished.\n")
    # The function returns the server response to use it later.
    return r.text


# Function that sends the HTTP POST request to the server and retrieves the raw data of the calendar.
def post_second_request(
    url, session_token, render_token, ajax, source, view, start, end, submit
):
    print("[@] Sending the calendar request...")

    # Cookies of the request.
    payload = {
        "JSESSIONID": session_token,
        "oam.Flash.RENDERMAP.TOKEN": render_token,
        "cookieconsent_status": "dismiss",
    }

    # Define variables of the request.
    string_start = source + "_start"
    string_end = source + "_end"
    string_submit = submit + "_SUBMIT"

    # Creating the body with the parameters extracted before, with the syntax required by the server.
    print("[*] Creating the payload...")
    body_payload = f"javax.faces.partial.ajax={ajax}&javax.faces.source={source}&javax.faces.partial.execute={source}&javax.faces.partial.render={source}&{source}={source}&{string_start}={start}&{string_end}={end}&{string_submit}=1&javax.faces.ViewState={view}"

    # Send the POST request.
    r = requests.post(
        url,
        data=body_payload,
        headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
        cookies=payload,
    )
    print("[#] Calendar request correctly retrieved.\n")

    # Write the raw response into a temporary file.
    print("[@] Writing the raw calendar data into a .txt file...")
    f = open("raw.txt", "w")
    f.write(r.text)
    f.close()
    print("[#] File correctly written.\n")