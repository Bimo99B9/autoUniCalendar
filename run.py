import epiCalendar
import os
import uuid
import utils
import re

from flask import Flask, render_template, request, send_file
app = Flask(__name__, static_folder='./build', static_url_path='/', template_folder='./build')

defaultFilename = epiCalendar.filename
debug = os.environ.get('FLASK_ENV') == 'development'

@app.route('/', methods = ['GET'])
def index():
    return serve()

@app.route('/', methods = ['POST'])
def form_post():
    if debug: print(f"[DEBUG] POST data received from React: {request.form}")

    jsessionid = request.form['jsessionid']
    filename = request.form['filename']
    location = request.form['location'] == "true"
    classType = request.form['class-type'] == "true"
    icsMode = request.form['extension'] == ".ics"

    if debug:
        print(f"[DEBUG] Calendar info: {jsessionid} → {filename}")
        print(f"[DEBUG] Location: {location}")
        print(f"[DEBUG] Class type: {classType}")
        print(f"[DEBUG] iCalendar mode: {icsMode}")

    if utils.verifyCookieExpiration(jsessionid):

        argv = ['epiCalendar.py', jsessionid]

        if not location: argv.append('--disable-location-parsing')
        if not classType: argv.append('--disable-class-type-parsing')

        uuidStr = str(uuid.uuid4())
        argv.append('-o')
        argv.append(uuidStr)

        # temporal csv fixes (ics not supported on web yet)
        if icsMode:
            backendFilename = uuidStr + '.ics'
            downloadFilename = filename + '.ics'
        else:
            argv.append("--csv")
            backendFilename = uuidStr + '.csv'
            downloadFilename = filename + '.csv'

        if debug:
            print(f"[DEBUG] UUID: {uuidStr}")
            print(f"[DEBUG] Arguments: {argv}")

        try:
            if epiCalendar.main(argv) == 0:
                if debug:
                    print(f"[DEBUG] Attempting to serve {backendFilename} as {downloadFilename}.")
                target = send_file(backendFilename, as_attachment=True, attachment_filename=downloadFilename)
                if os.path.exists(backendFilename): os.remove(backendFilename)
                return target
        except FileNotFoundError:
            print("[DEBUG] [ERROR] Exception occurred while generating/serving the calendar file.")
            return render_template('index.html', slug="ERROR: error al generar el calendario.")

    elif debug:
        print("[DEBUG] [ERROR] Expired cookie submited.")

    return render_template('index.html', slug="ERROR: cookie inválida.")


@app.errorhandler(404)
def serve():
    return render_template('index.html')
