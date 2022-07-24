import epiCalendar
import os
from flask import Flask, render_template, request, send_file
app = Flask(__name__)
defaultFilename = epiCalendar.csvFile

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods = ['POST'])
def index_post():
    jsessionid = request.form.get('jsessionid')
    filename = request.form.get('filename')
    settings = request.form.getlist('cb')

    filename = filename if filename else defaultFilename # if filename is not provided, use default

    if epiCalendar.verifyCookie(jsessionid):

        argv = ['epiCalendar.py', jsessionid]

        if not 'location' in settings: argv.append('--disable-location-parsing')
        if not 'class-type' in settings: argv.append('--disable-class-type-parsing')
        if not 'experimental-location' in settings: argv.append('--disable-experimental-location-parsing')

        if epiCalendar.main(argv) == 0:
            target = send_file(defaultFilename, as_attachment=True, attachment_filename=filename)
            if os.path.exists(filename): os.remove(filename)
            return target
        else:
            return render_template('index.html', slug_error='Something went wrong. Check your JSESSIONID and try again.')