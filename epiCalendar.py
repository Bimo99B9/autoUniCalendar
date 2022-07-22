#!/usr/bin/python3
# coding: utf-8

import re
import requests
import sys
import urllib.parse
import os
import time

# Declare global variables.
url = 'https://sies.uniovi.es/serviciosacademicos/web/expedientes/calendario.xhtml'
reg = '"([^"]*)"'
tmp = "epiTmpFile"
csvFile = "Calendario.csv"
rSession = requests.Session()

# Toggle location and class type parsing using the following global variables.
# If all special parsing is disabled, this script behaves almost exactly as the original one.
# If you intend to use this script for a non-EPI calendar, you should disable them all.
# Disabling location parsing will disable experimental location parsing.
enableLocationParsing = True
enableExperimentalLocationParsing = True
enableClassTypeParsing = True


def invalidChar():
    print("× (Invalid JSESSIONID)")
    exit(1)

# Function to send the first GET HTTP request using the tokens provided.
def get_first_request(session_token):

    print("Sending initial payload...", end=" ", flush=True)
    initTime = time.time()

    # Cookies payload of the HTTP request.
    payload = {
        'JSESSIONID': session_token,
        'cookieconsent_status': 'dismiss'
    }

    r = rSession.get(url, cookies=payload)
    print("✓ (%.3fs)" % (time.time() - initTime))

    # The function returns the server response to use it later.
    return r.text

# Function to extract the cookies necessary to make the POST request, from the server response of the first request.
def extract_cookies(get_response):
    print("Extracting cookies...", end=" ", flush=True)
    initTime = time.time()

    # Iterate the response lines to search the cookies, and save them in variables.
    found_first, found_second, found_third = False, False, False
    for line in get_response.split('\n'):
        if '<div id="j_id' in line and not found_first:
            source = urllib.parse.quote(re.findall(reg, line.split('<')[1])[0])
            found_first = True

        if 'javax.faces.ViewState' in line and not found_second:
            viewstate = urllib.parse.quote(re.findall(reg, line.split(' ')[12])[0])
            found_second = True

        if 'action="/serviciosacademicos/web/expedientes/calendario.xhtml"' in line and not found_third:
            submit = re.findall(reg, line.split(' ')[3])[0]
            found_third = True

    # The function returns a list that contains the extracted parameters.
    if not 'source' in locals():
        print("× (¿Invalid JSESSIONID?)")
        exit(1)
    print("✓ (%.3fs)" % (time.time() - initTime))
    return [source, viewstate, submit]

# Function that sends the HTTP POST request to the server and retrieves the raw data of the calendar.
def post_second_request(session_token, ajax, source, view, start, end, submit):

    print("Obtaining raw calendar data...", end=" ", flush=True)
    initTime = time.time()

    payload = {
        'JSESSIONID': session_token,
        'cookieconsent_status': 'dismiss'
    }

    # Define variables of the request.
    string_start = source + "_start"
    string_end = source + "_end"
    string_submit = submit + "_SUBMIT"

    # Creating the body with the parameters extracted before, with the syntax required by the server.
    body_payload = f"javax.faces.partial.ajax={ajax}&javax.faces.source={source}&javax.faces.partial.execute={source}&javax.faces.partial.render={source}&{source}={source}&{string_start}={start}&{string_end}={end}&{string_submit}=1&javax.faces.ViewState={view}"

    # Send the POST request.
    r = rSession.post(url, data=body_payload, headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}, cookies=payload)

    # Write the raw response into a temporary file.
    with open(tmp, 'w') as f: f.write(r.text)

    print("✓ (%.3fs)" % (time.time() - initTime))

# Parse the correct class name for each entry.
def parseLocation(loc):

    if not enableLocationParsing: return loc
    location = loc.rsplit()

    if location[1] == "Informática": return f"AN-{location[2]}"
    if location[1] == "De": return f"AN-{location[3]}"
    if "-" in location[1]:
        location = location[1].split("-")
        return f"{location[0].upper()}-{location[1]}"
    if location[0] == "Aula": return f"AN-{location[1]}"

    if not enableExperimentalLocationParsing: return loc
    # The following conditions are experimental and NOT thoroughly tested.
    i = 0
    while i < len(location):
        if "(" in location[i]: return f"DO {location[i]}"
        elif "BC" in location[i]: return f"DE {location[i]}"
        elif "." in location[i]: return f"EP {location[i]}"
        i += 1

    return loc # If the location is not recognized, return the original string.

# Parse the correct "class type" for each entry.
# AFAIKthere are only "Teoría (CEX)", "Prácticas de Aula (PA)", "Prácticas de Laboratorio (PL)" and "Teorías Grupales (TG)".
def parseClassType(type):

    if not enableClassTypeParsing: return type
    classType = type.replace('.','').replace('-', ' ').rsplit()

    if classType[0] == "Teoría": return f"CEX"
    if classType[1] == "Grupales": return f"TG{classType[2].strip('0')}"
    if classType[2] == "Aula": return f"PA{classType[3].strip('0')}"
    if classType[2] == "Laboratorio": return f"PL{classType[3].strip('0')}"

    return type # If the class type is not recognized, return the original string.

# Function that creates a CSV file readable by the applications, from the raw data previously retrieved.
def create_csv(file):

    print("Parsing data and generating new csv...", end=" ", flush=True)
    initTime = time.time()

    # Create the file.
    f = open(file, "r")
    g = open(csvFile, "w")

    # Write the headers in the first line.
    g.write("Asunto,Fecha de comienzo,Comienzo,Fecha de finalización,Finalización,Todo el día,Reminder on/off,Reminder Date,Reminder Time,Meeting Organizer,Required Attendees,Optional Attendees,Recursos de la reuniÃƒÂ³n,Billing Information,Categories,Description,Location,Mileage,Priority,Private,Sensitivity,Show time as\n")

    # Separate the events from its XML context.
    text = f.read().split('<')
    events = text[5].split('{')
    del events[0:2]

    # Each field of the event is separated by commas.
    for event in events:
        data = []
        for field in event.split(','):
            # Remove empty fields.
            if field.strip():
                data.append(field)
        # Save in variables the fields needed to build the CSV line of the event.
        title = data[1]
        start = data[2]
        end = data[3]
        description = data[7]

        # Make the necessary strings transformations to adapts the raw field data into a CSV readable file.
        title_csv = re.findall(reg, title.split(':')[1])[0]

        title = title_csv.split(" - ")[0]
        classType = parseClassType(title_csv.split(" - ")[1])
        title = f"{title} ({classType})"

        start_date = start.split(' ')[1].split('T')[0].split('"')[1]
        start_date_csv = start_date.split('-')[2]+'/'+start_date.split('-')[1]+'/'+start_date.split('-')[0]
        start_hour = start.split(' ')[1].split('T')[1].split('+')[0]
        end_date = end.split(' ')[1].split('T')[0].split('"')[1]
        end_date_csv = end_date.split('-')[2]+'/'+end_date.split('-')[1]+'/'+end_date.split('-')[0]
        end_hour = end.split(' ')[1].split('T')[1].split('+')[0]
        alert_date = start_date_csv
        alert_hour = str(int(start.split(' ')[1].split('T')[1].split('+')[0].split(':')[0]) - 1) + ':' + start.split(' ')[1].split('T')[1].split('+')[0].split(':')[1] + ':' + start.split(' ')[1].split('T')[1].split('+')[0].split(':')[2]
        event_creator = "Universidad de Oviedo"
        body = description.split('"')[3].replace(r'\n', '')

        info = body.split(" - ")[0]
        location = parseLocation(body.split(" - ")[1])

        # Write all the fields into a single line, and append it to the file.
        csv_line = f"{title},{start_date_csv},{start_hour},{end_date_csv},{end_hour},FALSO,FALSO,{alert_date},{alert_hour},{event_creator},,,,,,{info},{location},,Normal,Falso,Normal,2\n"
        g.write(csv_line)

    f.close() ; g.close()
    os.remove(tmp)
    print("✓ (%.3fs)" % (time.time() - initTime))

def verifyCookie(jsessionid) -> bool:
    if len(jsessionid) != 37: return False
    for i in range(4):
        if jsessionid[i] != "0": return False
    if jsessionid[27] != ":" or jsessionid[28] != "1" or jsessionid[29] != "d":
        return False
    return True

if __name__ == "__main__":
    session = ""

    # Read flags from arguments.
    if not len(sys.argv) == 1 and (sys.argv[1] == "--help" or sys.argv[1] == "-h"):
        print("Usage: python3 epiCalendar.py [JSESSIONID] [-o | --output-file <filename>] [--disable-location-parsing] [--disable-class-type-parsing] [--disable-experimental-location-parsing]")
        exit(0)

    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "--disable-location-parsing": enableLocationParsing = False
        if sys.argv[i] == "--disable-class-type-parsing": enableClassTypeParsing = False
        if sys.argv[i] == "--disable-experimental-location-parsing": enableExperimentalLocationParsing = False
        if sys.argv[i] == "-o" or sys.argv[i] == "--output-file" : csvFile = sys.argv[i+1]
        if verifyCookie(sys.argv[i]): session = sys.argv[i]

    # If the required argument hasn't been provided, read from input.
    if session == "":
        try:
            session = input("Enter JSESSIONID: ")
        except (KeyboardInterrupt, EOFError):
            exit(0)

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
first_request = get_first_request(session, render_map)
cookies = extract_cookies(first_request)
post_second_request(session, render_map, "true", cookies[0], cookies[1], "1662444000000", "1683612000000", cookies[2])
create_csv("raw.txt")
=======
cookies = extract_cookies(get_first_request(session, render_map))
post_second_request(session, render_map, "true", cookies[0], cookies[1], "1630886400000", "1652054400000", cookies[2])
create_csv(tmp)
<<<<<<< HEAD
>>>>>>> d7a59862 (console output, minor changes)
=======
>>>>>>> 729f7937 (EOF new line)
=======
=======
    # Cookie verification.
    if (len(session)) != 37: invalidChar()
    for i in range(4):
        if session[i] != "0": invalidChar()
    if session[27] != ":" or session[28] != "1" or session[29] != "d":
        invalidChar()

    startTime = time.time()
>>>>>>> fbbc953c (ajustado tiempo de ejecución, comprobación de cookie, readme)
    cookies = extract_cookies(get_first_request(session))
    post_second_request(session, "true", cookies[0], cookies[1], "1630886400000", "1652054400000", cookies[2])
    create_csv(tmp)
    print("\nCalendar generated, took %.3fs" % (time.time() - startTime))
>>>>>>> 0bf041e8 (cambios importantes)
