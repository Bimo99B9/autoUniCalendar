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


# Function that creates a CSV file readable by the applications, from the raw data previously retrieved.
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

        # Each field of the event is separated by commas.
        print("[*] Parsing the data...")
        for event in events:
            data = []
            for field in event.split(","):
                # Remove empty fields.
                if field.strip():
                    data.append(field)

            # Handle cases where data is missing by providing default values.
            title = data[1] if len(data) > 1 else '"title": "No Title"'
            start = data[2] if len(data) > 2 else '"start": "0000-00-00T00:00:00+0000"'
            end = data[3] if len(data) > 3 else '"end": "0000-00-00T00:00:00+0000"'
            description = data[7] if len(data) > 7 else '"description": "No description available"'

            # Use regular expressions to extract values from the fields.
            # This ensures that we can handle cases where the title has extra colons.
            title_match = re.search(r'"title":\s*"([^"]*)"', title)
            if title_match:
                title_csv = title_match.group(1)
            else:
                title_csv = "No Title"

            # Make the necessary string transformations to adapt the raw field data into a CSV-readable file.
            start_date = start.split(" ")[1].split("T")[0].split('"')[1]
            start_date_csv = (
                start_date.split("-")[2]
                + "/"
                + start_date.split("-")[1]
                + "/"
                + start_date.split("-")[0]
            )
            start_hour = start.split(" ")[1].split("T")[1].split("+")[0]
            end_date = end.split(" ")[1].split("T")[0].split('"')[1]
            end_date_csv = (
                end_date.split("-")[2]
                + "/"
                + end_date.split("-")[1]
                + "/"
                + end_date.split("-")[0]
            )
            end_hour = end.split(" ")[1].split("T")[1].split("+")[0]
            alert_date = start_date_csv
            alert_hour = (
                str(int(start.split(" ")[1].split("T")[1].split("+")[0].split(":")[0]) - 1)
                + ":"
                + start.split(" ")[1].split("T")[1].split("+")[0].split(":")[1]
                + ":"
                + start.split(" ")[1].split("T")[1].split("+")[0].split(":")[2]
            )
            event_creator = "Universidad de Oviedo"
            body = description.split('"')[3].replace(r"\n", "") if len(description.split('"')) > 3 else description

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
