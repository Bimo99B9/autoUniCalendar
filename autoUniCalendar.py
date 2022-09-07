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
buildingCodes = { # building codes for 'Milla del Conocimiento' (Gijón 02.01) sourced from gis.uniovi.es
    '01': 'AN',
    '02': 'AS',
    '04': 'DE',
    '05': 'DO',
    '08': 'EP'
}


# Function to send the first GET request using the cookie provided.
def getFirstRequest(jsessionid):

    print("Sending initial payload...", end=" ", flush=True)
    initTime = time.time()

    r = connect.firstRequest(jsessionid)
    if r.status_code != 200: errorOut("Unexpected response code")
    print("✓ (%.3fs)" % (time.time() - initTime))

    return r.text

# Function to extract the cookies necessary to make the POST request, from the server response of the first request.
def extractCookies(response):
    print("Extracting cookies...", end=" ", flush=True)
    initTime = time.time()

    # Iterate the response lines to search the cookies, and save them in variables.
    found_first, found_second, found_third = False, False, False
    for line in response.split('\n'):
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
        errorOut("Invalid JSESSIONID")

    print("✓ (%.3fs)" % (time.time() - initTime))
    return [source, viewstate, submit] # Return a list that contains the extracted parameters.

# Function that sends the HTTP POST request to the server and retrieves the raw data of the calendar.
# The raw text response is returned.
def postCalendarRequest(jsessionid, cookies):

    print("Obtaining raw calendar data...", end=" ", flush=True)
    initTime = time.time()

    e = datetime.now()
    start = int(datetime.timestamp(datetime(e.year if e.month >= 9 else e.year - 1, 9, 1)) * 1000)
    end = int(datetime.timestamp(datetime(e.year + 1 if e.month >= 9 else e.year, 6, 1)) * 1000)

    #start = 1598914597000
    #end = 1693522597000

    source = cookies[0]
    view = cookies[1]
    submit = cookies[2]

    # Creating the body with the parameters extracted before, with the syntax required by the server.
    calendarPayload = f"javax.faces.partial.ajax=true&javax.faces.source={source}&javax.faces.partial.execute={source}&javax.faces.partial.render={source}&{source}={source}&{source}_start={start}&{source}_end={end}&{submit}_SUBMIT=1&javax.faces.ViewState={view}"

    # Send the POST request.
    result = connect.postRequest(calendarPayload, jsessionid).text

    # Basic response verification.
    if result.split('<')[-1] != "/partial-response>":
        errorOut("Invalid response")

    try: sampleId = re.search(r'[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}', result).group(0)
    except AttributeError: print ("× (No calendar events)")

    locations = {}
    if enableLocationParsing:
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
def parseLocation(loc, codEspacio):

    #if not enableLocationParsing: return loc

    try: buildingCode = codEspacio.split('.')[2] # current building code
    except IndexError: # should never happen, but this way it's more robust.
        return loc

    floor = codEspacio.split('.')[4]
    if not codEspacio[:5] == "02.01" or not buildingCode in buildingCodes: return loc


    # Aula AS-1 through Aula AS-11
    result = re.search(r'02.01.02.00.P1.00.(0[1-9]|1[0-1])', codEspacio)
    if bool(result):
        return f"AS-{loc.split('-')[1]}"

    # Parse 'Sala Informática Px', 'Aula de Informática Bx' , 'Aula Informática Sx' and 'Aula Bx' from Aulario Norte.
    result = re.search(r'02.01.01.00.((P1.00.0[3-6])|(P0.00.01.((1[2-7])|(0[189])))|(S1.00.(0[45789]|1[023])))', codEspacio)
    if bool(result):
        return f"AN-{loc.split(' ')[-1].upper()}"

    # Parse 'Aula A' through 'Aula E' from Aulario Norte.
    result = re.search(r'02.01.01.00.P1.00.((0[7-9])|(1[0-1]))', codEspacio)
    if bool(result):
        return f"AN-{loc.split(' ')[-1].upper()}"

    # Parse rooms with standard room codes (x.x.xx)
    result = re.search(r'\d\...?\.\d\d', loc)
    if bool(result):
        return f"{buildingCodes[buildingCode]}-{result.group(0)}"

    # Parse 'Aula DO-1' through 'Aula DO -17'
    # No code-specific parsing is needed, names are unique and easily identifiable.
    # Same goes for Departamental Este below.
    result = re.search(r'^AULA DO[ ]?-1?\d[A-B]?$', loc.upper())
    if bool(result):
        doFinal = result.group(0).replace('AULA ', '').replace(' ', '')
        if doFinal[-2:] == "10": # DO-10 can be DO-10A or DO-10B.
            return f"{doFinal}{loc[-1]}"
        return doFinal

    # Parse 'Aula DE-1' through 'Aula DE-8'.
    result = re.search(r'^AULA DE-[1-8]$', loc.upper())
    if bool(result):
        return f"{result.group(0).replace('AULA ', '')}"

    # Parse Aula A2 through A6 and Aula A1 through A8 from Edificio Polivalente.
    result = re.search(r'02.01.08.00.P((1.00.06.0[1-5])|(0.00.0[2-9]))', codEspacio)
    if bool(result):
        return f"EP-{loc.split(' ')[-1].upper()}"


    # If no match is found, return the original name including building and floor.
    return f"{buildingCodes[buildingCode]}-{loc} ({floor})"

# Parse the correct "class type" for each entry.
# Also parses the group for each entry except for "Clase Expositiva".
# AFAIK there are only "Teoría (CEX)", "Prácticas de Aula (PAx)", "Prácticas de Laboratorio (PLx)" and "Teorías Grupales (TGx)".
def parseClassType(type):

    if not enableClassTypeParsing: return type
    typeL = type.lower().replace('.', '')
    classGroup = type.replace('-', ' ').rsplit()[-1].strip('0').upper()
    if classGroup == "INGLÉS": classGroup = "🇬🇧"
    lang = "🇬🇧" if "inglés" in typeL or "ingles" in typeL else ""

    if "teo" in typeL or typeL == "te" or "expositiv" in typeL: return f"CEX{lang}"
    if "tut" in typeL or "grupal" in typeL or typeL == "tg": return f"TG{classGroup}"
    if "lab" in typeL or typeL == "pl": return f"PL{classGroup}"
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
        g.write("Subject,Start Date,Start Time,End Date,End Time,Location,Description\n")

    # Each field of the event is separated by commas.
    for event in events:
        data = []
        for field in event.split(','):
            # Remove empty fields.
            if field.strip():
                data.append(field)
        # Save in variables the fields needed to build the CSV line of the event.
        uid = data[0].split('": "')[1].replace('"', '')
        title = data[1].split('": "')[1].replace('"', '')
        start = data[2].split('": "')[1].replace('T', ' ').replace('"', '').split('+')[0]
        end = data[3].split('": "')[1].replace('T', ' ').replace('"', '').split('+')[0]
        description = data[7].split('":"')[1].replace(r'\n', '').replace('"}', '').replace(']}]]>', '')

        titleSplit = title.split(" - ")
        classType = parseClassType(titleSplit[1])
        title = f"{titleSplit[0]} ({classType})"

        start_date = start.split(' ')[0]
        start_hour = start.split(' ')[1]
        end_date = end.split(' ')[0]
        end_hour = end.split(' ')[1]

        loc = description.split(" - ")[1]
        location = parseLocation(loc, locations[loc.lower()].split('?codEspacio=')[1])
        if enableLinks: description += f" ({locations[loc.lower()]})"

        # Update the statistics.
        stats["classes"] += 1
        if enableStatistics:
            hours = int(end_hour.split(':')[0]) - int(start_hour.split(':')[0])
            minutes = int(end_hour.split(':')[1]) - int(start_hour.split(':')[1])
            hours = hours + minutes / 60
            print(hours)
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
            csv_line = f"{title},{start_date},{start_hour},{end_date},{end_hour},{location},{description}\n"
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
        print("Usage: python3 autoUniCalendar.py [JSESSIONID]")
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

    # If the JSESSIONID is not valid, exit.
    if not utils.verifyCookieStructure(session):
        errorOut("Invalid JSESSIONID.")

    startTime = time.time()
    try:
        cookies = extractCookies(getFirstRequest(session))
        rawResponse, locations = postCalendarRequest(session, cookies)
        stats = generateCalendar(rawResponse, locations)
    except UnboundLocalError:
        return 2

    print("\n%s, took %.3fs (%d events parsed)" % ("Dry run completed" if dryRun else "Calendar generated", time.time() - startTime, stats["classes"]))
    ext = "ics" if icsMode else "csv"
    if not dryRun: print(f"Saved as \"{filename}.{ext}\"")

    if enableStatistics:
        print("\nStatistics:")
        print("\tClasses: %d" % stats["classes"])
        print("\tHours: %.2f" % stats["hours"])
        print("\tDays of attendance: %d" % len(stats["days"]))

        print("\tAverage hours per day: %.2f" % (stats["hours"] / len(stats["days"])))
        print("\tMax hours per day: %.2f" % max(stats["days"].values()))

        print("\tFirst quarter: %d classes (%.2f hours)" % (stats["Q1"][0], stats["Q1"][1]))
        print("\tSecond quarter: %d classes (%.2f hours)" % (stats["Q2"][0], stats["Q2"][1]))

        print("\n\tClass types:")
        for classType in stats["classTypes"]:
            print("\t\t%s: %d (%.2fh)" % (classType[0], classType[1][0], classType[1][1]))

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
            print("\t\t%s: %d (%.2fh)" % (location[0], location[1][0], location[1][1]))

        if enableLocationParsing:
            print("\t\tGlobal locations:")
            for location in globalLocations:
                if globalLocations[location][0] != 0: print("\t\t\t%s: %d (%dh)" % (location, globalLocations[location][0], globalLocations[location][1]))

        print("\n\tSubjects:")
        for subject in stats["subjects"]:
            print("\t\t%s: %d (%.2fh)" % (subject, stats["subjects"][subject][0], stats["subjects"][subject][1]))


    return 0

def errorOut(message):
    print(f"× ({message})")
    exit(1)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
