#!/usr/bin/python3
# coding: utf-8

import re
import requests
import sys
import urllib.parse
import os

if len(sys.argv) != 3:
    print(
        f"\n[!] Uso: python3 {sys.argv[0]} <JSESSIONID> <RENDER_MAP.TOKEN>\n")
    sys.exit(1)

session = sys.argv[1]
render_map = sys.argv[2]

print("[i] autoUniCalendar, is a script which converts the Uniovi calendar into Google and Microsoft calendars.")
print("[i] Designed and programmed by Daniel López Gala from the University of Oviedo.")
print("[i] Visit Bimo99B9.github.io for more content.")
print(f"[*] The provided session is: {session}")
print(f"[*] The provided render token is: {render_map}")

URL = 'https://sies.uniovi.es/serviciosacademicos/web/expedientes/calendario.xhtml'


def get_uniovi_calendar_info(session, token):
    [source, view, submit] = extract_cookies()

    print("[@] Sending the calendar request...")

    payload = {
        'JSESSIONID': session,
        'oam.Flash.RENDER_MAP.TOKEN': token,
        'cookieconsent_status': 'dismiss'
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

    print("[*] Creating the payload...")

    body_payload = f"javax.faces.partial.ajax=true&javax.faces.source={source}&javax.faces.partial.execute={source}&javax.faces.partial.render={source}&{source}={source}&{source}_start=1630886400000&{source}_end=1652054400000&{submit}_SUBMIT=1&javax.faces.ViewState={view}"

    request = requests.post(URL, data=body_payload,
                            headers=headers, cookies=payload)

    print("[#] Calendar request correctly retrieved.")

    print("[@] Writing the raw calendar data into a .txt file...")

    file = open("raw.txt", "w")
    file.write(request.text)
    file.close()

    print("[#] File correctly written.")


def extract_cookies():
    req = first_uniovi_request(session, render_map)
    print("[@] Extracting the calendar parameters...")
    for line in req.split('\n'):
        if '<div id="j_id' in line:
            tmp = line.split('<')
            src = tmp[1]
            src2 = re.findall('"([^"]*)"', src)[0]
            source = urllib.parse.quote(src2)
            print(f"[*] javax.faces.source retrieved: {source}")
            break

    for line in req.split('\n'):
        if 'javax.faces.ViewState' in line:
            tmp = line
            st = tmp.split(' ')[12]
            viewst = re.findall('"([^"]*)"', st)[0]
            viewstate = urllib.parse.quote(viewst)
            print(f"[*] javax.faces.ViewState retrieved: {viewstate}")
            break

    for line in req.split('\n'):
        if 'action="/serviciosacademicos/web/expedientes/calendario.xhtml"' in line:
            tmp = line.split(' ')
            submit = re.findall('"([^"]*)"', tmp[3])[0]
            print(f"[*] javax.faces.source_SUBMIT retrieved: {submit}")
            break

    print("[#] Calendar parameters extracted.")

    return [source, viewstate, submit]


def first_uniovi_request(session, token):
    print("[@] Sending the first request...")

    payload = {
        'JSESSIONID': session,
        'oam.Flash.RENDER_MAP.TOKEN': token
    }

    request = requests.get(URL, cookies=payload)

    print("[#] First request correctly finished.")

    return request.text


def create_csv_file():
    print("[@] Creating the CSV file...")
    file = open("raw.txt", "r")
    csv_file = open("Calendario.CSV", "w")
    csv_file.write("Asunto,Fecha de comienzo,Comienzo,Fecha de finalización,Finalización,Todo el dí­a,Reminder on/off,Reminder Date,Reminder Time,Meeting Organizer,Required Attendees,Optional Attendees,Recursos de la reuniÃƒÂ³n,Billing Information,Categories,Description,Location,Mileage,Priority,Private,Sensitivity,Show time as\n")
    data = file.read()
    text = data.split('<')
    calendar = text[5]
    events = calendar.split('{')
    del events[0:2]

    print("[*] Parsing the data...")
    for event in events:
        res = []
        for ele in event.split(','):
            if ele.strip():
                res.append(ele)
        title = res[1]
        start = res[2]
        end = res[3]
        description = res[7]

        title = re.findall('"([^"]*)"', title.split(':')[1])[0]

        tmp = start.split(' ')[1].split('T')[0].removeprefix('"')

        start_date = tmp.split('-')[2]+'/' + \
            tmp.split('-')[1]+'/'+tmp.split('-')[0]

        start_hour = start.split(' ')[1].split('T')[1].split('+')[0]

        tmp = end.split(' ')[1].split('T')[0].removeprefix('"')

        end_date = tmp.split('-')[2]+'/' + \
            tmp.split('-')[1]+'/'+tmp.split('-')[0]

        alert_hour = str(int(start.split(' ')[1].split('T')[1].split('+')[0].split(':')[0]) - 1) + ':' + start.split(' ')[
            1].split('T')[1].split('+')[0].split(':')[1] + ':' + start.split(' ')[1].split('T')[1].split('+')[0].split(':')[2]

        creator = "Universidad de Oviedo"

        body = description.split('"')[3].replace(r'\n', '')

        csv_line = f"{title},{start_date},{start_hour},{end_date},{start_date},FALSO,FALSO,{start_date},{alert_hour},{creator},,,,,,,{body},,,Normal,Falso,Normal,2\n"

        csv_file.write(csv_line)

    print("[*] Events correctly written in the CSV file.")

    file.close()
    csv_file.close()

    print("[*] Removing raw .txt file...")

    os.remove("raw.txt")

    print("[#] Calendar generated. You can now import it in Outlook or Google Calendar selecting 'import from file' and providing the CSV file generated.")


get_uniovi_calendar_info(session, render_map)

create_csv_file()
