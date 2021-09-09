#!/usr/bin/python3
# coding: utf-8

import re
import requests
import sys
import urllib.parse
import os

if len(sys.argv) != 3:
    print("\n[!] Uso: python3 " + sys.argv[0] + " <JSESSIONID> <RENDERMAP.TOKEN>\n")
    sys.exit(1)

session = sys.argv[1]
rendermap = sys.argv[2]

print("[i] autoUniCalendar, a script to convert the Uniovi calendar to Google and Microsoft calendars.")
print("[i] Designed and programmed by Daniel López Gala from the University of Oviedo.")
print("[i] Visit Bimo99B9.github.io for more content.\n")
print("\n[*] The provided session is: " + session)
print("[*] The provided render token is: " + rendermap + "\n")


# print(session + rendermap)

def get_first_request(s, r):
    print("[@] Sending the first request...")
    url = 'https://sies.uniovi.es/serviciosacademicos/web/expedientes/calendario.xhtml'
    payload = {
        'JSESSIONID': s,
        'oam.Flash.RENDERMAP.TOKEN': r
    }
    r = requests.get(url, cookies=payload)
    print("[#] First request correctly finished.\n")
    return r.text


def extract_cookies(req):
    print("[@] Extracting the calendar parameters...")
    for line in req.split('\n'):
        if '<div id="j_id' in line:
            tmp = line.split('<')
            src = tmp[1]
            src2 = re.findall('"([^"]*)"', src)[0]
            source = urllib.parse.quote(src2)
            print("[*] javax.faces.source retrieved: " + source)
            break

    for line in req.split('\n'):
        if 'javax.faces.ViewState' in line:
            tmp = line
            st = tmp.split(' ')[12]
            viewst = re.findall('"([^"]*)"', st)[0]
            viewstate = urllib.parse.quote(viewst)
            print("[*] javax.faces.ViewState retrieved: " + viewstate)
            break

    for line in req.split('\n'):
        if 'action="/serviciosacademicos/web/expedientes/calendario.xhtml"' in line:
            tmp = line.split(' ')
            submit = re.findall('"([^"]*)"', tmp[3])[0]
            print("[*] javax.faces.source_SUBMIT retrieved: " + submit)
            break

    print("[#] Calendar parameters extracted.\n")

    return [source, viewstate, submit]


def post_second_request(s, r, ajax, source, view, start, end, submit):
    print("[@] Sending the calendar request...")

    url = 'https://sies.uniovi.es/serviciosacademicos/web/expedientes/calendario.xhtml'
    payload = {
        'JSESSIONID': s,
        'oam.Flash.RENDERMAP.TOKEN': r,
        'cookieconsent_status': 'dismiss'
    }
    stringstart = source + "_start"
    stringend = source + "_end"
    stringsubmit = submit + "_SUBMIT"
    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

    print("[*] Creating the payload...")
    bodypayload = "javax.faces.partial.ajax=" + ajax + "&javax.faces.source=" + source + "&javax.faces.partial.execute=" + source + "&javax.faces.partial.render=" + source + "&" + source + "=" + source + "&" + stringstart + "=" + start + "&" + stringend + "=" + end + "&" + stringsubmit + "=1&javax.faces.ViewState=" + view

    r = requests.post(url, data=bodypayload, headers=headers, cookies=payload)
    print("[#] Calendar request correctly retrieved.\n")

    print("[@] Writing the raw calendar data into a .txt file...")
    f = open("raw.txt", "w")
    f.write(r.text)
    f.close()
    print("[#] File correctly written.\n")


def treatFile(file):

    print("[@] Creating the CSV file...")
    f = open(file, "r")
    g = open("Calendario.CSV", "w")
    g.write("Asunto,Fecha de comienzo,Comienzo,Fecha de finalización,Finalización,Todo el dí­a,Reminder on/off,Reminder Date,Reminder Time,Meeting Organizer,Required Attendees,Optional Attendees,Recursos de la reuniÃƒÂ³n,Billing Information,Categories,Description,Location,Mileage,Priority,Private,Sensitivity,Show time as\n")
    data = f.read()
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
        id = res[0]
        title = res[1]
        start = res[2]
        end = res[3]
        allday = res[4]
        editable = res[5]
        className = res[6]
        description = res[7]

        titulo = re.findall('"([^"]*)"', title.split(':')[1])[0]
        tmp = start.split(' ')[1].split('T')[0].removeprefix('"')
        fechainicio = tmp.split('-')[2]+'/'+tmp.split('-')[1]+'/'+tmp.split('-')[0]
        horainicio = start.split(' ')[1].split('T')[1].split('+')[0]
        tmp = end.split(' ')[1].split('T')[0].removeprefix('"')
        fechafin = tmp.split('-')[2]+'/'+tmp.split('-')[1]+'/'+tmp.split('-')[0]
        horafin = end.split(' ')[1].split('T')[1].split('+')[0]
        fechadealerta = fechainicio
        horadealerta = str(int(start.split(' ')[1].split('T')[1].split('+')[0].split(':')[0]) - 1) + ':' + start.split(' ')[1].split('T')[1].split('+')[0].split(':')[1] + ':' + start.split(' ')[1].split('T')[1].split('+')[0].split(':')[2]
        creador = "Universidad de Oviedo"
        body = re.findall('"([^"]*)"', description.split(':')[1].replace(r'\n', ''))[0]

        csvline = titulo+','+fechainicio+','+horainicio+','+fechafin+','+horafin+',FALSO,FALSO,'+fechadealerta+','+horadealerta+','+creador+',,,,,,'+body+',,,Normal,Falso,Normal,2\n'
        g.write(csvline)
    print("[*] Events correctly written in the CSV file.")
    f.close()
    g.close()
    print("[*] Removing raw .txt file...")
    os.remove("raw.txt")
    print("\n[#] Calendar generated. You can now import it in Outlook or Google Calendar selecting 'import from file' and providing the CSV file generated.\n")


first_request = get_first_request(session, rendermap)
cookies = extract_cookies(first_request)
post_second_request(session, rendermap, "true", cookies[0], cookies[1], "1630886400000", "1652054400000", cookies[2])
treatFile("raw.txt")
