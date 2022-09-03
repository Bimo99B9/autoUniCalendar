#!/usr/bin/python3
# coding: utf-8

import re
from webbrowser import get
import requests
import sys
import urllib.parse
import os
import time

from flask import Flask, render_template, request, send_file
import gunicorn

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    #return render_template('index.html')

    cookie1 = request.form.get('cookie1')
    cookie2 = request.form.get('cookie2')

    user = request.form.get('user')
    password = request.form.get('password')

    if(cookie1 != None and cookie2 != None):
        autoUniCalendar_cookies(cookie1, cookie2)
        time.sleep(1)
        return send_file("Calendario.CSV", as_attachment=True, attachment_filename="Calendario.CSV")

    if(user != None and password != None):
        autoUniCalendar_login(user, password)
        time.sleep(1)
        return send_file("Calendario.CSV", as_attachment=True, attachment_filename="Calendario.CSV")

    return render_template('index.html')
    return render_template("form.html")
    
'''
Get the CSV calendar with the user and password
of the user.
'''
def autoUniCalendar_login(user, password):
    user = user
    password = password

    # With the credentials, retrieve the cookies and use them as if
    # the cookies had been provided
    def getCookies(user, password):
        print()
        # TODO Create the algorithm.
        cookie1 = ""
        cookie2 = ""

        autoUniCalendar_cookies(cookie1, cookie2)

    
'''
Get the CSV calendar with the user cookies.
'''
def autoUniCalendar_cookies(cookie1, cookie2):

    # Declare global variables.
    url = 'https://sies.uniovi.es/serviciosacademicos/web/expedientes/calendario.xhtml'
    session = cookie1
    render_map = cookie2

    # Script information.
    print("[i] autoUniCalendar, a script which converts the Uniovi calendar into Google and Microsoft calendars.")
    print("[i] Designed and programmed by Daniel López Gala from the University of Oviedo.")
    print("[i] Visit Bimo99B9.github.io for more content.\n")
    print(f"[*] The provided session cookie is: {session}")
    print(f"[*] The provided render token is: {render_map}")

    # Function to send the first GET HTTP request using the tokens provided.
    def get_first_request(session_token, render_token):

        print("[@] Sending the first request...")

        # Cookies payload of the HTTP request.
        payload = {
            'JSESSIONID': session_token,
            'oam.Flash.RENDERMAP.TOKEN': render_token
        }

        r = requests.get(url, cookies=payload)
        print("[#] First request correctly finished.\n")
        # The function returns the server response to use it later.
        return r.text

    # Function to extract the cookies necessary to make the POST request, from the server response of the first request.
    def extract_cookies(get_response):
        print("[@] Extracting the calendar parameters...")

        # Iterate the response lines to search the cookies, and save them in variables.

        found_first, found_second, found_third = False, False, False
        for line in get_response.split('\n'):
            if '<div id="j_id' in line and not found_first:
                source = urllib.parse.quote(re.findall('"([^"]*)"', line.split('<')[1])[0])
                found_first = True

            if 'javax.faces.ViewState' in line and not found_second:
                viewstate = urllib.parse.quote(re.findall('"([^"]*)"', line.split(' ')[12])[0])
                found_second = True

            if 'action="/serviciosacademicos/web/expedientes/calendario.xhtml"' in line and not found_third:
                submit = re.findall('"([^"]*)"', line.split(' ')[3])[0]
                found_third = True

        print("[#] Calendar parameters extracted.\n")
        # The function returns a list that contains the extracted parameters.
        return [source, viewstate, submit]

    # Function that sends the HTTP POST request to the server and retrieves the raw data of the calendar.
    def post_second_request(session_token, render_token, ajax, source, view, start, end, submit):

        print("[@] Sending the calendar request...")
        
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
        print("[*] Creating the payload...")
        body_payload = f"javax.faces.partial.ajax={ajax}&javax.faces.source={source}&javax.faces.partial.execute={source}&javax.faces.partial.render={source}&{source}={source}&{string_start}={start}&{string_end}={end}&{string_submit}=1&javax.faces.ViewState={view}"

        # Send the POST request. 
        r = requests.post(url, data=body_payload, headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}, cookies=payload)
        print("[#] Calendar request correctly retrieved.\n")

        # Write the raw response into a temporary file.
        print("[@] Writing the raw calendar data into a .txt file...")
        f = open("raw.txt", "w")
        f.write(r.text)
        f.close()
        print("[#] File correctly written.\n")

    # Function that creates a CSV file readable by the applications, from the raw data previously retrieved.
    def create_csv(file):

        print("[@] Creating the CSV file...")
        
        # Create the file.
        f = open(file, "r")
        g = open("Calendario.CSV", "w")

        # Write the headers in the first line.
        g.write("Asunto,Fecha de comienzo,Comienzo,Fecha de finalización,Finalización,Todo el dí­a,Reminder on/off,Reminder Date,Reminder Time,Meeting Organizer,Required Attendees,Optional Attendees,Recursos de la reuniÃƒÂ³n,Billing Information,Categories,Description,Location,Mileage,Priority,Private,Sensitivity,Show time as\n")
        
        # Separate the events from its XML context.
        text = f.read().split('<')
        events = text[5].split('{')
        del events[0:2]

        # Each field of the event is separated by commas.
        print("[*] Parsing the data...")
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
            title_csv = re.findall('"([^"]*)"', title.split(':')[1])[0]
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
            # Write all the fields into a single line, and append it to the file.
            csv_line = f"{title_csv},{start_date_csv},{start_hour},{end_date_csv},{end_hour},FALSO,FALSO,{alert_date},{alert_hour},{event_creator},,,,,,{body},,,Normal,Falso,Normal,2\n"
            g.write(csv_line)
            
        print("[*] Events correctly written in the CSV file.")
        f.close()
        g.close()
        print("[*] Removing raw .txt file...")
        os.remove("raw.txt")
        print("\n[#] Calendar generated. You can now import it in Outlook or Google Calendar selecting 'import from file' and providing the CSV file generated.\n")


    first_request = get_first_request(session, render_map)
    cookies = extract_cookies(first_request)
    post_second_request(session, render_map, "true", cookies[0], cookies[1], "1662444000000", "1683612000000", cookies[2])    
    create_csv("raw.txt")

