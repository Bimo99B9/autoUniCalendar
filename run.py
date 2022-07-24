import epiCalendar
import os
import uuid
import utils
from flask import Flask, render_template, request, send_file
app = Flask(__name__, static_folder='./build', static_url_path='/')
defaultFilename = epiCalendar.csvFile
uuidStr = ""

@app.route('/', methods = ['GET'])
def index():
    global uuidStr
    uuidStr = str(uuid.uuid4())
    return serve()

@app.route('/', methods = ['POST'])
def form_post():

    print(request.get_data())
    jsessionid = request.form.get('jsessionid')
    filename = request.form.get('filename')
    settings = request.form.getlist('cb')

    filename = filename + '.csv' if filename else defaultFilename # if filename is not provided, use default

    if utils.verifyCookieExpiration(jsessionid):

        argv = ['epiCalendar.py', jsessionid]

        if not 'location' in settings: argv.append('--disable-location-parsing')
        if not 'class-type' in settings: argv.append('--disable-class-type-parsing')
        if not 'experimental-location' in settings: argv.append('--disable-experimental-location-parsing')

        argv.append('-o')
        argv.append(uuidStr)

        if epiCalendar.main(argv) == 0:
            target = send_file(uuidStr, as_attachment=True, attachment_filename=filename)
            os.remove(uuidStr)
            return target

    return serve()

@app.errorhandler(404)
def serve():
    return app.send_static_file('index.html')