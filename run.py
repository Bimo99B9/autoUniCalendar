import epiCalendar
import os
import uuid
from flask import Flask, render_template, request, send_file
app = Flask(__name__)
defaultFilename = epiCalendar.csvFile
uuidStr = ""

@app.route('/', methods = ['GET'])
def index():
    global uuidStr
    uuidStr = str(uuid.uuid4())
    return render_template('index.html')

@app.route('/', methods = ['POST'])
def form_post():
    jsessionid = request.form.get('jsessionid')
    filename = request.form.get('filename')
    settings = request.form.getlist('cb')

    filename = filename + '.csv' if filename else defaultFilename # if filename is not provided, use default

    if epiCalendar.verifyCookie(jsessionid):

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

    return render_template('index.html', slug_error='Something went wrong. Check your JSESSIONID and try again.')