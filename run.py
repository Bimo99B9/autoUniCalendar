import epiCalendar
import os
from flask import Flask, render_template, request, send_file
app = Flask(__name__)
defaultFilename = epiCalendar.csvFile

@app.route('/', methods = ['GET', 'POST'])
def index():

    jsessionid = request.form.get('jsessionid')
    filename = request.form.get('filename')
    filename = filename if filename else defaultFilename
    print(f"{jsessionid} → {filename}")

    if epiCalendar.verifyCookie(jsessionid):
        if os.path.exists(defaultFilename): os.remove(defaultFilename)
        epiCalendar.main(['epiCalendar.py', jsessionid])
        return send_file(defaultFilename, as_attachment=True, attachment_filename=filename)
        if os.path.exists(defaultFilename): os.remove(defaultFilename)

    return render_template('index.html')
