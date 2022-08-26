#!/usr/bin/python3
# coding: utf-8

import re
import sys
import urllib.parse
import os
import time
import calendar
from ics import Calendar, Event # needed to save calendar in .ics format (iCalendar)
from datetime import datetime # needed to convert academic years to unix timestamps

# import custom modules
import connect
import utils

# Declare global variables.
reg = '"([^"]*)"'
filename = "Calendario" # Can be changed through "-o" flag.


# Function to send the first GET request using the cookie provided.
def getFirstRequest(jsessionid):

    print("Sending initial payload...", end=" ", flush=True)
    initTime = time.time()

    r = connect.firstRequest(jsessionid)
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

    e = datetime.now()
    start = int(datetime.timestamp(datetime(e.year if e.month >= 9 else e.year - 1, 9, 1))*1000)
    end = int(datetime.timestamp(datetime(e.year + 1 if e.month >= 9 else e.year, 6, 1))*1000)

    source = cookies[0]
    view = cookies[1]
    submit = cookies[2]

    # Creating the body with the parameters extracted before, with the syntax required by the server.
    calendarPayload = f"javax.faces.partial.ajax=true&javax.faces.source={source}&javax.faces.partial.execute={source}&javax.faces.partial.render={source}&{source}={source}&{source}_start={start}&{source}_end={end}&{submit}_SUBMIT=1&javax.faces.ViewState={view}"

    # Send the POST request.
    result = connect.postRequest(calendarPayload, jsessionid).text

    # Basic response verification.
    if result.split('<')[-1] != "/partial-response>":
        print("× (Invalid response)")
        exit(1)

    locations = {}
    if enableLinks:
        sampleId = re.search(r'[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}', result).group(0)
        locationPayload = f"javax.faces.partial.ajax=true&javax.faces.source={source}&javax.faces.partial.execute={source}&javax.faces.partial.render={source[:10:]}eventDetails+{source[:10:]}aulas_url&javax.faces.behaviour.event=eventSelect&javax.faces.partial.event=eventSelect&{source}_selectedEventId={sampleId}&{submit}_SUBMIT=1&javax.faces.ViewState={view}"

        locationInfo = connect.postRequest(locationPayload, jsessionid).text
        removeCharacters = ['\t', '\n', 'class="enlaceUniovi"', '</li>', '</a>', '<a href=', 'target="_blank">' , '"']
        for char in removeCharacters:
            locationInfo = locationInfo.replace(char, '')

        locationInfo = locationInfo.split('<li>')[1:]
        locationInfo[-1] = locationInfo[-1].split('</ul>')[0]

        for location in locationInfo:
            locations[location.split('  ')[1].lower()] = location.split('  ')[0]

    print("✓ (%.3fs)" % (time.time() - initTime))
    return result, locations



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
        "days": {},
        "classTypes": {},
        "locations": {},
        "subjects": {},
        "Q1": [0, 0],
        "Q2": [0, 0]
    }

    # Separate the events from its XML context.
    text = rawResponse.split('<')
    events = text[5].split('{')
    del events[0:2]

    if icsMode:
        c = Calendar()
    elif not dryRun:
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
            hours = int(end_hour.split(':')[0]) - int(start_hour.split(':')[0])
            stats["classes"] += 1
            stats["hours"] += hours

            if classType not in stats["classTypes"]:
                stats["classTypes"][classType] = [0, 0]

            if location not in stats["locations"]:
                stats["locations"][location] = [0, 0]

            if start_date not in stats["days"]:
                stats["days"][start_date] = 0

            if titleSplit[0] not in stats["subjects"]:
                stats["subjects"][titleSplit[0]] = [0, 0]

            stats["classTypes"][classType][0] += 1
            stats["classTypes"][classType][1] += hours
            stats["locations"][location][0] += 1
            stats["locations"][location][1] += hours
            stats["days"][start_date] += hours
            stats["subjects"][titleSplit[0]][0] += 1
            stats["subjects"][titleSplit[0]][1] += hours

            if int(start_date.split('-')[1]) >= 9:
                stats["Q1"][0] += 1
                stats["Q1"][1] += hours
            else:
                stats["Q2"][0] += 1
                stats["Q2"][1] += hours

        if icsMode:
            e = Event(name=title, begin=start, end=end, description=description, location=location, uid=uid)
            c.events.add(e)
        else:
            csv_line = f"{title},{start_date},{start_hour},{end_date},{end_hour},{description},{location}\n"
            if not dryRun: g.write(csv_line)

    if not dryRun:
        if icsMode:
            with open(filename + ".ics", "w") as f:
                f.writelines(c.serialize_iter())
        else:
            g.close()

    print("%s (%.3fs)" % ("~" if dryRun else "✓", time.time() - initTime))

    # Sort the class types and locations by number of occurrences.
    stats["classTypes"] = sorted(stats["classTypes"].items(), key=lambda x: x[1], reverse=True)
    stats["locations"] = sorted(stats["locations"].items(), key=lambda x: x[1], reverse=True)

    return stats

def main(argv) -> int:
    global enableLocationParsing, enableClassTypeParsing, enableStatistics, filename, icsMode, enableLinks, dryRun
    # Toggle location and class type parsing using the following global variables.
    # If all special parsing is disabled, this script behaves almost exactly as the original one.
    # If you intend to use this script for a non-EPI calendar, you should disable them all.
    # This options can be easily toggled through argument flags.
    enableLocationParsing = True
    enableClassTypeParsing = True
    enableLinks = True
    enableStatistics = False
    icsMode = True
    dryRun = False

    session = ""

    # Read flags from arguments.
    if "--help" in argv or "-h" in argv:
        print("Usage: python3 epiCalendar.py [JSESSIONID]")
        print("\nFLAGS:")
        print("\t[--disable-location-parsing]: Disables the parsing of the location of the class.")
        print("\t[--disable-class-type-parsing]: Disables the parsing of the class type of the class.")
        print("\t[--disable-links]: Disables placing links of rooms in the description of the events.")
        print("\t[--enable-statistics | -s | --stats]: Returns various statistics about all the events collected.")
        print("\t[--csv]: saves the calendar as a CSV file instead of an iCalendar file.")
        print("\t[--dry-run]: blocks any file from being created.")
        print("\t[--help], -h: shows this help message.")
        print("\t[--output-file | -o]: sets the name of the output file.")
        return 0

    for i in range(1, len(argv)):
        if argv[i] == "--disable-location-parsing": enableLocationParsing = False
        if argv[i] == "--disable-class-type-parsing": enableClassTypeParsing = False
        if argv[i] == "--disable-links": enableLinks = False
        if argv[i] == "--csv": icsMode = False
        if argv[i] == "-o" or argv[i] == "--output-file" : filename = argv[i+1]
        if argv[i] == "-s" or argv[i] == "--stats" or argv[i] == "--enable-statistics": enableStatistics = True
        if argv[i] == "--dry-run": dryRun = True
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
    print("\n%s, took %.3fs" % ("Dry run completed" if dryRun else "Calendar generated", time.time() - startTime))
    ext = "ics" if icsMode else "csv"
<<<<<<< HEAD
    print(f"Saved as \"{filename}.{ext}\"")
>>>>>>> c9a6a02f (support iCalendar format (default), other fixes)
=======
    if not dryRun: print(f"Saved as \"{filename}.{ext}\"")
>>>>>>> cddd3715 (dry run mode, better statistics)

    if enableStatistics:
        print("\nStatistics:")
        print("\tClasses: %d" % stats["classes"])
        print("\tHours: %d" % stats["hours"])
        print("\tDays of attendance: %d" % len(stats["days"]))

        print("\tAverage hours per day: %.2f" % (stats["hours"] / len(stats["days"])))
        print("\tMax hours per day: %d" % max(stats["days"].values()))

        print("\tFirst quarter: %d classes (%d hours)" % (stats["Q1"][0], stats["Q1"][1]))
        print("\tSecond quarter: %d classes (%d hours)" % (stats["Q2"][0], stats["Q2"][1]))

        print("\n\tClass types:")
        for classType in stats["classTypes"]:
            print("\t\t%s: %d (%dh)" % (classType[0], classType[1][0], classType[1][1]))

        globalLocations = {
            "Aulario Norte": [0, 0],
            "Aulario Sur": [0, 0],
            "Departamental Oeste": [0, 0],
            "Departamental Este": [0, 0],
            "Edificio Polivalente": [0, 0]
        }

        print("\n\tLocations:")
        for location in stats["locations"]:
            if enableLocationParsing:
                if location[0][:2] == "AN":
                    globalLocations["Aulario Norte"][0] += location[1][0]
                    globalLocations["Aulario Norte"][1] += location[1][1]
                elif location[0][:2] == "AS":
                    globalLocations["Aulario Sur"][0] += location[1][0]
                    globalLocations["Aulario Sur"][1] += location[1][1]
                elif location[0][:2] == "DO":
                    globalLocations["Departamental Oeste"][0] += location[1][0]
                    globalLocations["Departamental Oeste"][1] += location[1][1]
                elif location[0][:2] == "DE":
                    globalLocations["Departamental Este"][0] += location[1][0]
                    globalLocations["Departamental Este"][1] += location[1][1]
                elif location[0][:2] == "EP":
                    globalLocations["Edificio Polivalente"][0] += location[1][0]
                    globalLocations["Edificio Polivalente"][1] += location[1][1]
            print("\t\t%s: %d (%dh)" % (location[0], location[1][0], location[1][1]))

        if enableLocationParsing:
            print("\t\tGlobal locations:")
            for location in globalLocations:
                if globalLocations[location][0] != 0: print("\t\t\t%s: %d (%dh)" % (location, globalLocations[location][0], globalLocations[location][1]))

        print("\n\tSubjects:")
        for subject in stats["subjects"]:
            print("\t\t%s: %d (%dh)" % (subject, stats["subjects"][subject][0], stats["subjects"][subject][1]))


>>>>>>> 613083fe (better class type parsing, stats)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
>>>>>>> e87fc758 (estructura general, form html)
