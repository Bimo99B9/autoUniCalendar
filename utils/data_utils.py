# Function to extract the cookies necessary to make the POST request, from the server response of the first request.
import re
import urllib.parse
import os


def extract_cookies(get_response):
    print("[@] Extracting the calendar parameters...")

    # Iterate the response lines to search the cookies, and save them in variables.

    found_first, found_second, found_third = False, False, False
    for line in get_response.split("\n"):
        if '<div id="j_id' in line and not found_first:
            source = urllib.parse.quote(re.findall('"([^"]*)"', line.split("<")[1])[0])
            found_first = True

        if "javax.faces.ViewState" in line and not found_second:
            viewstate = urllib.parse.quote(
                re.findall('"([^"]*)"', line.split(" ")[12])[0]
            )
            found_second = True

        if (
            'action="/serviciosacademicos/web/expedientes/calendario.xhtml"' in line
            and not found_third
        ):
            submit = re.findall('"([^"]*)"', line.split(" ")[3])[0]
            found_third = True

    print("[#] Calendar parameters extracted.\n")
    # The function returns a list that contains the extracted parameters.
    return [source, viewstate, submit]


import re


def create_csv(file):
    print("[@] Creating the CSV file...")

    # Create the file.
    with open(file, "r") as f, open("Calendario.CSV", "w") as g:

        # Write the headers in the first line.
        g.write(
            "Asunto,Fecha de comienzo,Comienzo,Fecha de finalización,Finalización,Todo el dí­a,Reminder on/off,Reminder Date,Reminder Time,Meeting Organizer,Required Attendees,Optional Attendees,Recursos de la reuniÃƒÂ³n,Billing Information,Categories,Description,Location,Mileage,Priority,Private,Sensitivity,Show time as\n"
        )

        # Separate the events from its XML context.
        text = f.read().split("<")
        events = text[5].split("{")
        del events[0:2]

        print("[*] Parsing the data...")
        for event in events:
            data = {}

            # Use regular expressions to extract key-value pairs for each event
            matches = re.findall(r'"(\w+)":\s*"(.*?)"', event)
            for match in matches:
                key, value = match
                data[key] = value

            # Handle cases where data is missing by providing default values.
            title = data.get("title", "No Title")
            start = data.get("start", "0000-00-00T00:00:00+0000")
            end = data.get("end", "0000-00-00T00:00:00+0000")
            description = data.get("description", "No description available")

            # Ensure title is properly handled even with commas
            title_csv = title

            # Transform start and end date-time fields into CSV format
            start_date = start.split("T")[0]
            start_date_csv = "/".join(
                start_date.split("-")[::-1]
            )  # Convert from yyyy-mm-dd to dd/mm/yyyy
            start_hour = start.split("T")[1].split("+")[0]

            end_date = end.split("T")[0]
            end_date_csv = "/".join(
                end_date.split("-")[::-1]
            )  # Convert from yyyy-mm-dd to dd/mm/yyyy
            end_hour = end.split("T")[1].split("+")[0]

            # Alert is set 1 hour before the start time
            alert_date = start_date_csv
            alert_hour = (
                str(int(start_hour.split(":")[0]) - 1)
                + ":"
                + start_hour.split(":")[1]
                + ":"
                + start_hour.split(":")[2]
            )
            event_creator = "Universidad de Oviedo"
            body = description.replace(r"\n", "").strip()

            # Write all the fields into a single line, and append it to the file.
            csv_line = f"{title_csv},{start_date_csv},{start_hour},{end_date_csv},{end_hour},FALSO,FALSO,{alert_date},{alert_hour},{event_creator},,,,,,{body},,,Normal,Falso,Normal,2\n"
            g.write(csv_line)

    print("[*] Events correctly written in the CSV file.")

    # Remove the raw file.
    os.remove(file)
    print("[*] Removing raw file...")

    print(
        "\n[#] Calendar generated. You can now import it in Outlook or Google Calendar by selecting 'import from file' and providing the CSV file generated.\n"
    )
