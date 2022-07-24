import epiCalendar
import os
import uuid
import utils
import re
from flask import Flask, render_template, request, send_file
app = Flask(__name__, static_folder='./build', static_url_path='/')
defaultFilename = epiCalendar.csvFile
uuidStr = ""

@app.route('/', methods = ['GET'])
def index():
    global uuidStr
    uuidStr = str(uuid.uuid4()) # Generate a random UUID for the session.
    return serve()

@app.route('/', methods = ['POST'])
def form_post():

    body = re.split(':|,', str(request.get_data())[3:-2].replace('"', ""))
    print(body)

    for i in range(len(body)):
        if body[i] == "jsessionid":
            jsessionid = body[i+1] + ":" + body[i+2]
        elif body[i] == "filename":
            filename = body[i+1] + ".csv"

    print(f"{jsessionid} → {filename}")

    settings = request.form.getlist('cb')

    if utils.verifyCookieExpiration(jsessionid):

        argv = ['epiCalendar.py', jsessionid]

        if not 'location' in settings: argv.append('--disable-location-parsing')
        if not 'class-type' in settings: argv.append('--disable-class-type-parsing')
        if not 'experimental-location' in settings: argv.append('--disable-experimental-location-parsing')

        #if os.path.exists(defaultFilename): os.remove(defaultFilename)
        if epiCalendar.main(argv) == 0:
           target = send_file(defaultFilename, as_attachment=True, attachment_filename=filename)
           #if os.path.exists(defaultFilename): os.remove(defaultFilename)
           return target

    return serve()


@app.errorhandler(404)
def serve():
    return app.send_static_file('index.html')
