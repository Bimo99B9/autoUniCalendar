#!/usr/bin/python3
# coding: utf-8

import re
import requests
import sys
import urllib.parse
import os
import time
import utils
import calendar
from ics import Calendar, Event
from datetime import datetime

# Declare global variables.
url = 'https://sies.uniovi.es/serviciosacademicos/web/expedientes/calendario.xhtml'
reg = '"([^"]*)"'
filename = "Calendario" # Can be changed through "-o" flag.
rSession = requests.Session()

# Toggle location and class type parsing using the following global variables.
# If all special parsing is disabled, this script behaves almost exactly as the original one.
# If you intend to use this script for a non-EPI calendar, you should disable them all.
# This options can be easily toggled through argument flags.
enableLocationParsing = True
enableClassTypeParsing = True
enableLinks = True
enableStatistics = False
icsMode = True



# Function to send the first GET request using the cookie provided.
def getFirstRequest(session_token):

    print("Sending initial payload...", end=" ", flush=True)
    initTime = time.time()

    payload = {
        'JSESSIONID': session_token,
        'cookieconsent_status': 'dismiss'
    }

    r = rSession.get(url, cookies=payload)
    print("✓ (%.3fs)" % (time.time() - initTime))

    return r.text

# Function to extract the cookies necessary to make the POST request, from the server response of the first request.
def extractCookies(get_response):
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

        if found_first and found_second and found_third: break

    if not 'source' in locals(): # If the variable 'source' is not defined, the cookie was probably not valid.
        print("× (¿Invalid JSESSIONID?)")
        exit(1)

    print("✓ (%.3fs)" % (time.time() - initTime))
    return [source, viewstate, submit] # Return a list that contains the extracted parameters.

# Function that sends the HTTP POST request to the server and retrieves the raw data of the calendar.
# The raw text response is returned.
def postCalendarRequest(jsessionid, cookies):

    print("Obtaining raw calendar data...", end=" ", flush=True)
    initTime = time.time()

    payload = {
        'JSESSIONID': jsessionid,
        'cookieconsent_status': 'dismiss'
    }

    e = datetime.now()
    start = int(datetime.timestamp(datetime(e.year if e.month >= 9 else e.year - 1, 9, 1))*1000)
    end = int(datetime.timestamp(datetime(e.year + 1 if e.month >= 9 else e.year, 6, 1))*1000)

    source = cookies[0]
    view = cookies[1]
    submit = cookies[2]

    # Creating the body with the parameters extracted before, with the syntax required by the server.
    calendarPayload = f"javax.faces.partial.ajax=true&javax.faces.source={source}&javax.faces.partial.execute={source}&javax.faces.partial.render={source}&{source}={source}&{source}_start={start}&{source}_end={end}&{submit}_SUBMIT=1&javax.faces.ViewState={view}"

    # Send the POST request.
    result = postRequest(calendarPayload, payload).text

    # Basic response verification.
    if result.split('<')[-1] != "/partial-response>":
        print("× (Invalid response)")
        exit(1)

    locations = {}
    if enableLinks:
        sampleId = re.search(r'[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}', result).group(0)
        locationPayload = f"javax.faces.partial.ajax=true&javax.faces.source={source}&javax.faces.partial.execute={source}&javax.faces.partial.render={source[:10:]}eventDetails+{source[:10:]}aulas_url&javax.faces.behaviour.event=eventSelect&javax.faces.partial.event=eventSelect&{source}_selectedEventId={sampleId}&{submit}_SUBMIT=1&javax.faces.ViewState={view}"

        locationInfo = postRequest(locationPayload, payload).text
        removeCharacters = ['\t', '\n', 'class="enlaceUniovi"', '</li>', '</a>', '<a href=', 'target="_blank">' , '"']
        for char in removeCharacters:
            locationInfo = locationInfo.replace(char, '')

        locationInfo = locationInfo.split('<li>')[1:]
        locationInfo[-1] = locationInfo[-1].split('</ul>')[0]

        for location in locationInfo:
            locations[location.split('  ')[1].lower()] = location.split('  ')[0]

    print("✓ (%.3fs)" % (time.time() - initTime))
    return result, locations

def postRequest(payload, cookiePayload):
    return rSession.post(url, data=payload, headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}, cookies=cookiePayload)

# Parse the correct class name for each entry.
def parseLocation(loc):

    if not enableLocationParsing: return loc

    # Parse Aula AS-1 through Aula AS-11. (sometimes Aula As-X instead of Aula AS-X)
    asResult = re.search(r'A[Ss]-\d\d?', loc)
    if bool(asResult):
        return asResult.group(0).upper()

    # Parse 'Sala Informática Px', 'Aula de Informática Bx' , 'Aula Informática Sx' and 'Aula Bx'.
    # Also parses 'Aula Bx' from Edificio Polivalente incorrectly, but there is no way to tell them apart from the data.
    anResult = re.search(r'[PBS]\d', loc)
    if bool(anResult):
        return f"AN-{anResult.group(0)}"

    # Parse rooms from Edificio Polivalente using their code (format: X.X.XX)
    epResult = re.search(r'\d\.\d\.\d\d', loc)
    if bool(epResult):
        return f"EP-{epResult.group(0)}"

    # Parse 'Aula DE-1' through 'Aula DE-8'.
    deResult = re.search(r'DE-\d', loc)
    if bool(deResult):
        return f"{deResult.group(0)}"

    # Parse 'Aula DO-1' through 'Aula DO -17'
    doResult = re.search(r'DO[ ]?-\d\d?', loc)
    if bool(doResult):
        doFinal = doResult.group(0).replace(' ', '')
        if doFinal[-2:] == "10": # DO-10 can be DO-10A or DO-10B.
            return f"{doFinal}{loc[-1]}"
        return doFinal

    # Parse rooms from Departamental Oeste (Bajo cubierta) using their code (format: X.BC.XX)
    # Very similar codes to the EP rooms, can be difficult to parse.
    doResult = re.search(r'(\d.BC.\d\d)|(\d.S.\d\d)|(\d.B.\d\d)', loc)
    if bool(doResult):
        return f"DO-{doResult.group(0)}"

    # Parse 'Aula A' through 'Aula E'.
    # Has to be last because it is very generic and could match other locations.
    aeResult = re.search(r'Aula [A-E]', loc)
    if bool(aeResult):
        return f"AN-{aeResult.group(0)[-1]}"

    return loc

# Parse the correct "class type" for each entry.
# Also parses the group for each entry except for "Clase Expositiva".
# AFAIK there are only "Teoría (CEX)", "Prácticas de Aula (PAx)", "Prácticas de Laboratorio (PLx)" and "Teorías Grupales (TGx)".
def parseClassType(type):

    if not enableClassTypeParsing: return type
    typeL = type.lower()
    classGroup = type.replace('-', ' ').rsplit()[-1].strip('0').upper()
    if classGroup == "INGLÉS": classGroup = "🇬🇧"
    lang = "🇬🇧" if "inglés" in typeL or "ingles" in typeL else ""

    if "teoría" in typeL or typeL == "te": return f"CEX{lang}"
    if "tutoría" in typeL or "grupal" in typeL or typeL == "tg": return f"TG{classGroup}"
    if "laboratorio" in typeL or typeL == "pl": return f"PL{classGroup}"
    if "aula" in typeL or typeL == "pa": return f"PA{classGroup}"

    return type # If the class type is not recognized, return the original string.

def generateCalendar(rawResponse, locations):

    print("Parsing data and creating calendar...", end=" ", flush=True)
    initTime = time.time()

    stats = {
        "hours": 0,
        "classes": 0,
        "classTypes": {},
        "locations": {}
    }

    # Separate the events from its XML context.
    text = rawResponse.split('<')
    events = text[5].split('{')
    del events[0:2]

    if icsMode:
        c = Calendar()
    else:
        g = open(filename + ".csv", "w")
        g.write("Subject,Start Date,Start Time,End Date,End Time,Description,Location\n")

    # Each field of the event is separated by commas.
    for event in events:
        data = []
        for field in event.split(','):
            # Remove empty fields.
            if field.strip():
                data.append(field)
        # Save in variables the fields needed to build the CSV line of the event.
        uid = data[0].split(': ')[1].replace('"', '')
        title = data[1].split(': ')[1].replace('"', '')
        start = data[2].split(': ')[1].replace('T', ' ').replace('"', '').split('+')[0]
        end = data[3].split(': ')[1].replace('T', ' ').replace('"', '').split('+')[0]
        description = data[7].split('"')[3].replace(r'\n', '')

        titleSplit = title.split(" - ")
        classType = parseClassType(titleSplit[1])
        title = f"{titleSplit[0]} ({classType})"

        start_date = start.split(' ')[0]
        start_hour = start.split(' ')[1]
        end_date = end.split(' ')[0]
        end_hour = end.split(' ')[1]

        loc = description.split(" - ")[1]
        location = parseLocation(loc)
        if enableLinks: description += f" ({locations[loc.lower()]})"

        # Update the statistics.
        if enableStatistics:
            stats["classes"] += 1
            stats["hours"] += int(end_hour.split(':')[0]) - int(start_hour.split(':')[0])
            if classType not in stats["classTypes"]:
                stats["classTypes"][classType] = 1
            else:
                stats["classTypes"][classType] += 1
            if location not in stats["locations"]:
                stats["locations"][location] = 1
            else:
                stats["locations"][location] += 1

        if icsMode:
            e = Event(name=title, begin=start, end=end, description=description, location=location, uid=uid)
            c.events.add(e)
        else:
            csv_line = f"{title},{start_date},{start_hour},{end_date},{end_hour},{description},{location}\n"
            g.write(csv_line)

    if icsMode:
        with open(filename + ".ics", "w") as f:
            f.writelines(c.serialize_iter())
    else:
        g.close()

    print("✓ (%.3fs)" % (time.time() - initTime))

    # Sort the class types and locations by number of occurrences.
    stats["classTypes"] = sorted(stats["classTypes"].items(), key=lambda x: x[1], reverse=True)
    stats["locations"] = sorted(stats["locations"].items(), key=lambda x: x[1], reverse=True)

    return stats

def main(argv) -> int:
    global enableLocationParsing, enableClassTypeParsing, enableStatistics, filename, icsMode, enableLinks
    session = ""

    # Read flags from arguments.
    if "--help" in argv or "-h" in argv:
        print("Usage: python3 epiCalendar.py [JSESSIONID] [-o | --output-file <filename>] [--disable-location-parsing] [--disable-class-type-parsing]")
        return 0

    for i in range(1, len(argv)):
        if argv[i] == "--disable-location-parsing": enableLocationParsing = False
        if argv[i] == "--disable-class-type-parsing": enableClassTypeParsing = False
        if argv[i] == "--disable-links": enableLinks = False
        if argv[i] == "--csv": icsMode = False
        if argv[i] == "-o" or argv[i] == "--output-file" : filename = argv[i+1]
        if argv[i] == "-s" or argv[i] == "--stats" or argv[i] == "--enable-statistics": enableStatistics = True
        if utils.verifyCookieStructure(argv[i]): session = argv[i]

    # If the required argument hasn't been provided, read from input.
    if session == "":
        try:
            session = input("Enter JSESSIONID: ")
        except (KeyboardInterrupt, EOFError):
            return 0

<<<<<<< HEAD
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
=======
    # If the JSESSIONID is not valid, exit.
    if not utils.verifyCookieStructure(session):
        print("× Invalid JSESSIONID.")
<<<<<<< HEAD
        exit(1)
>>>>>>> 8d8cb67e (it works!)
=======
        return 1
>>>>>>> c9a6a02f (support iCalendar format (default), other fixes)

    startTime = time.time()
<<<<<<< HEAD
>>>>>>> fbbc953c (ajustado tiempo de ejecución, comprobación de cookie, readme)
    cookies = extract_cookies(get_first_request(session))
    post_second_request(session, "true", cookies[0], cookies[1], "1630886400000", "1652054400000", cookies[2])
    create_csv(tmp)
=======
    cookies = extractCookies(getFirstRequest(session))
<<<<<<< HEAD
<<<<<<< HEAD
    createCsv(postCalendarRequest(session, "true", cookies[0], cookies[1], "1630886400000", "1652054400000", cookies[2]))
>>>>>>> 542ef996 (removal of temp files, verifications/optimizations)
=======
    stats = createCsv(postCalendarRequest(session, "true", cookies[0], cookies[1], "1630886400000", "1652054400000", cookies[2]))
>>>>>>> 613083fe (better class type parsing, stats)
=======
    rawResponse, locations = postCalendarRequest(session, cookies)
<<<<<<< HEAD
<<<<<<< HEAD
    stats = createCsv(rawResponse)
>>>>>>> 2b1fc7ee (obtain links for each location , english parsing, other minor changes)
=======
    stats = createCsv(rawResponse, locations)
>>>>>>> 47c7e784 (reduce csv length, add link to location)
    print("\nCalendar generated, took %.3fs" % (time.time() - startTime))
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 0bf041e8 (cambios importantes)
=======
=======
    print("Saved as \"%s\"" % csvFile)
<<<<<<< HEAD
>>>>>>> dea54aa3 (f/b comms, no settings and no download)
=======
=======
    stats = generateCalendar(rawResponse, locations)
    print("\nCalendar generated, took %.3fs" % (time.time() - startTime))
    ext = "ics" if icsMode else "csv"
    print(f"Saved as \"{filename}.{ext}\"")
>>>>>>> c9a6a02f (support iCalendar format (default), other fixes)

    if enableStatistics:
        print("\nStatistics:")
        print("\tClasses: %d" % stats["classes"])
        print("\tHours: %d" % stats["hours"])
        print("\tClass types:")
        for classType in stats["classTypes"]:
            print("\t\t%s: %d" % (classType[0], classType[1]))
        print("\tLocations:")
        for location in stats["locations"]:
            print("\t\t%s: %d" % (location[0], location[1]))

>>>>>>> 613083fe (better class type parsing, stats)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
>>>>>>> e87fc758 (estructura general, form html)
