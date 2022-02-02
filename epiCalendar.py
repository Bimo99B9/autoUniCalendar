#!/usr/bin/python3
# coding: utf-8

import re
import requests
import sys
import urllib.parse
import os

# Check if the required arguments have been provided, and indicate the use of the script.
if len(sys.argv) != 3:
    print("\n[!] Uso: python3 " + sys.argv[0] + " <JSESSIONID> <RENDERMAP.TOKEN>\n")
    sys.exit(1)

# Declare global variables.
url = 'https://sies.uniovi.es/serviciosacademicos/web/expedientes/calendario.xhtml'
session = sys.argv[1]
render_map = sys.argv[2]
reg = '"([^"]*)"'
tmp = "epiTmpFile"

# Script information.
#print(f"Using {session} and {render_map} as cookies.")

# Function to send the first GET HTTP request using the tokens provided.
def get_first_request(session_token, render_token):

    print("Sending the first request...", end=" ")

    # Cookies payload of the HTTP request.
    payload = {
        'JSESSIONID': session_token,
        'oam.Flash.RENDERMAP.TOKEN': render_token
    }

    r = requests.get(url, cookies=payload)
    print("✅")
    # The function returns the server response to use it later.
    return r.text

# Function to extract the cookies necessary to make the POST request, from the server response of the first request.
def extract_cookies(get_response):
    print("Extracting calendar parameters...", end=" ")

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

    print("✅")
    # The function returns a list that contains the extracted parameters.
    try:
        return [source, viewstate, submit]
    except UnboundLocalError:
        print("Couldn't extract calendar parameters. (¿Invalid cookies?)")
        exit(1)

# Function that sends the HTTP POST request to the server and retrieves the raw data of the calendar.
def post_second_request(session_token, render_token, ajax, source, view, start, end, submit):

    print("Sending the calendar request...", end=" ")
    
    # Cookies of the request.
    payload = {
        'JSESSIONID': session_token,
        'oam.Flash.RENDERMAP.TOKEN': render_token,
        'cookieconsent_status': 'dismiss'
    }

    # Define variables of the request.
    string_start = source + "_start"
    string_end = source + "_end"
    string_submit = submit + "_SUBMIT"

    # Creating the body with the parameters extracted before, with the syntax required by the server.
    body_payload = f"javax.faces.partial.ajax={ajax}&javax.faces.source={source}&javax.faces.partial.execute={source}&javax.faces.partial.render={source}&{source}={source}&{string_start}={start}&{string_end}={end}&{string_submit}=1&javax.faces.ViewState={view}"

    # Send the POST request. 
    r = requests.post(url, data=body_payload, headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}, cookies=payload)
    print("✅")

    # Write the raw response into a temporary file.
    print("Writing the raw calendar data to a temp file...", end=" ")
    f = open(tmp, "w")
    f.write(r.text)
    f.close()
    print("✅")

# Function that creates a CSV file readable by the applications, from the raw data previously retrieved.
def create_csv(file):

    print("Creating csv file...", end=" ")
    
    # Create the file.
    f = open(file, "r")
    g = open("Calendario.csv", "w")

    print("✅")

    # Write the headers in the first line.
    g.write("Asunto,Fecha de comienzo,Comienzo,Fecha de finalización,Finalización,Todo el día,Reminder on/off,Reminder Date,Reminder Time,Meeting Organizer,Required Attendees,Optional Attendees,Recursos de la reuniÃƒÂ³n,Billing Information,Categories,Description,Location,Mileage,Priority,Private,Sensitivity,Show time as\n")
    
    # Separate the events from its XML context.
    text = f.read().split('<')
    events = text[5].split('{')
    del events[0:2]

    # Each field of the event is separated by commas.
    print("Parsing the data...", end=" ")
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
        classType = title_csv.split(" - ")[1].replace('.','').replace('-', ' ').rsplit()
        if classType[0] == "Teoría": classType = f"CEX"
        elif classType[1] == "Grupales": classType = f"TG{classType[2  ].strip('0')}"
        elif classType[2] == "Aula": classType = f"PA{classType[3].strip('0')}"
        elif classType[2] == "Laboratorio": classType = f"PL{classType[3].strip('0')}"
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
        location = body.split(" - ")[1].rsplit()
        
        if location[1] == "Informática": location = f"AN-{location[2]}"
        elif location[1] == "De": location = f"AN-{location[3]}"
        elif "-" in location[1]:
            location = location[1].split("-")
            location = f"{location[0].upper()}-{location[1]}"
        elif "." in location[1]: location = f"EP {location[1]}"
        elif len(location) > 2 and "." in location[2]: location = f"EP {location[2]}"
        elif location[0] == "Aula": location = f"AN-{location[1]}"

        # Write all the fields into a single line, and append it to the file.
        csv_line = f"{title},{start_date_csv},{start_hour},{end_date_csv},{end_hour},FALSO,FALSO,{alert_date},{alert_hour},{event_creator},,,,,,{info},{location},,Normal,Falso,Normal,2\n"
        g.write(csv_line)
        
    print("✅")
    f.close()
    g.close()
    print("Removing temp file...", end=" ")
    os.remove(tmp)
    print("✅")
    print("\nCalendar generated.\n")


<<<<<<< HEAD
first_request = get_first_request(session, render_map)
cookies = extract_cookies(first_request)
post_second_request(session, render_map, "true", cookies[0], cookies[1], "1662444000000", "1683612000000", cookies[2])
create_csv("raw.txt")
=======
cookies = extract_cookies(get_first_request(session, render_map))
post_second_request(session, render_map, "true", cookies[0], cookies[1], "1630886400000", "1652054400000", cookies[2])
create_csv(tmp)
>>>>>>> d7a59862 (console output, minor changes)
