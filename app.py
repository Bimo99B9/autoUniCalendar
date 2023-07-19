#!/usr/bin/python3
# coding: utf-8

import time
from flask import Flask, render_template, request, send_file
from flask_talisman import Talisman
from utils.http_utils import get_first_request, post_second_request
from utils.data_utils import extract_cookies, create_csv

app = Flask(__name__)

Talisman(app, content_security_policy=None)


@app.route("/", methods=["GET", "POST"])
def index():
    # return render_template('index.html')

    cookie1 = request.form.get("cookie1")
    cookie2 = request.form.get("cookie2")

    user = request.form.get("user")
    password = request.form.get("password")

    if cookie1 != None and cookie2 != None:
        autoUniCalendar_cookies(cookie1, cookie2)
        time.sleep(1)
        return send_file(
            "Calendario.CSV", as_attachment=True, download_name="Calendario.CSV"
        )

    if user != None and password != None:
        pass
        # autoUniCalendar_login(user, password)
        # time.sleep(1)
        # return send_file(
        #     "Calendario.CSV", as_attachment=True, download_name="Calendario.CSV"
        # )

    return render_template("index.html")



# Get the CSV calendar with the user and password of the user.
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


# Get the CSV calendar with the user cookies.
def autoUniCalendar_cookies(cookie1, cookie2):
    # Declare global variables.
    SIES_URL = (
        "https://sies.uniovi.es/serviciosacademicos/web/expedientes/calendario.xhtml"
    )
    JSESSIONID = cookie1
    RENDERMAP = cookie2

    # Script information.
    print(
        "[i] autoUniCalendar, a script which converts the Uniovi calendar into Google and Microsoft calendars."
    )
    print(
        "[i] Designed and programmed by Daniel López Gala from the University of Oviedo."
    )
    print("[i] Visit Bimo99B9.github.io for more content.\n")
    

    first_request = get_first_request(SIES_URL, JSESSIONID, RENDERMAP)
    cookies = extract_cookies(first_request)
    post_second_request(
        SIES_URL,
        JSESSIONID,
        RENDERMAP,
        "true",
        cookies[0],
        cookies[1],
        "1662444000000",
        "1683612000000",
        cookies[2],
    )
    create_csv("raw.txt")
