import autoUniCalendar
import os
import uuid
import utils
import re


from flask import Flask, render_template, request, send_file
from flask_talisman import Talisman
app = Flask(__name__)
Talisman(app, content_security_policy=None)

defaultFilename = autoUniCalendar.filename
debug = os.environ.get('FLASK_ENV') == 'development'

@app.route('/', methods = ['GET'])
def index():
    return serve()

@app.route('/', methods = ['POST'])
def form_post():
    if debug: print(f"[DEBUG] POST data received: {request.form}")

    jsessionid = request.form.get('cookie1')
    filename = defaultFilename
    location = True
    classType = True
    extension = ".csv" # change to csv mode for now

    if debug:
        print(f"[DEBUG] Calendar info: {jsessionid} → {filename}{extension}")
        print(f"[DEBUG] Location parsing: {location}")
        print(f"[DEBUG] Class type parsing: {classType}")
        print(f"[DEBUG] iCalendar mode: {extension == '.ics'}")

    """
    if not utils.verifyCookieExpiration(jsessionid):
        print("[DEBUG] [ERROR] Expired cookie submited.")
        # an exception should not be raised in backend, but there is no way to communicate with frontend yet.
        return serve(error="ERROR Invalid cookie submited.")
    """


    argv = ['autoUniCalendar.py', jsessionid]

    if not location: argv.append('--disable-location-parsing')
    if not classType: argv.append('--disable-class-type-parsing')

    uuidStr = str(uuid.uuid4())
    argv.append('-o')
    argv.append(uuidStr)

    backendFilename = uuidStr + extension
    downloadFilename = filename + extension
    if extension == ".csv": argv.append('--csv')

    if debug:
        print(f"[DEBUG] UUID: {uuidStr}")
        print(f"[DEBUG] Arguments: {argv}")

    exitCode = autoUniCalendar.main(argv)
    if os.path.exists(backendFilename) and exitCode == 0:
        if debug: print(f"[DEBUG] Attempting to serve {backendFilename} as {downloadFilename}.")
        target = send_file(backendFilename, as_attachment=True, attachment_filename=downloadFilename)
        if os.path.exists(backendFilename): os.remove(backendFilename)
        if debug: print(f"[DEBUG] File served.")
        return target
    elif exitCode == 2:
        if debug: print("[DEBUG] [ERROR] ¿No calendar events?")
        return serve(error="ERROR: No hay eventos en el calendario.")
    if debug:
        print("[DEBUG] [ERROR] Script failed to generate file.")
        return serve(error="ERROR: No se pudo generar el calendario.")

    return serve()


@app.errorhandler(404)
def serve(error=""):
    return render_template('index.html', errormsg=error)
