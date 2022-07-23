import epiCalendar
import os
from flask import Flask, render_template, request, send_file
app = Flask(__name__)
defaultFilename = epiCalendar.csvFile

@app.route('/', methods = ['GET', 'POST'])
def index():

    jsessionid = request.form.get('jsessionid')
    filename = request.form.get('filename')
    settings = request.form.getlist('cb')

    filename = filename if filename else defaultFilename # if filename is not provided, use default

    if epiCalendar.verifyCookie(jsessionid):
        if os.path.exists(defaultFilename): os.remove(defaultFilename)
        argv = ['epiCalendar.py', jsessionid]

        if not 'location' in settings: argv.append('--disable-location-parsing')
        if not 'class-type' in settings: argv.append('--disable-class-type-parsing')
        if not 'experimental-location' in settings: argv.append('--disable-experimental-location-parsing')

        epiCalendar.main(argv)
        return send_file(defaultFilename, as_attachment=True, attachment_filename=filename)


    return render_template('index.html')
