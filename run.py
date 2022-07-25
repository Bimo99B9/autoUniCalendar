import epiCalendar
import os
import uuid
import utils
import re

from flask import Flask, render_template, request, send_file
app = Flask(__name__, static_folder='./build', static_url_path='/')

defaultFilename = epiCalendar.csvFile
debug = os.environ.get('FLASK_ENV') == 'development'

@app.route('/', methods = ['GET'])
def index():
    return serve()

@app.route('/', methods = ['POST'])
def form_post():
    if debug: print(request.form)

    jsessionid = request.form['jsessionid']
    filename = request.form['filename'] + ".csv"
    settings = ""

    if debug: print(f"{jsessionid} → {filename}")

    if utils.verifyCookieExpiration(jsessionid):

        argv = ['epiCalendar.py', jsessionid]

        if not 'location' in settings: argv.append('--disable-location-parsing')
        if not 'class-type' in settings: argv.append('--disable-class-type-parsing')
        if not 'experimental-location' in settings: argv.append('--disable-experimental-location-parsing')

        uuidStr = str(uuid.uuid4())
        argv.append('-o')
        argv.append(uuidStr)
        if debug:
            print(uuidStr)
            print(argv)

        try:
            if epiCalendar.main(argv) == 0:
                target = send_file(uuidStr, as_attachment=True, attachment_filename=filename)
                if os.path.exists(uuidStr): os.remove(uuidStr)
                return target
        except FileNotFoundError:
            print("Error temporal (¿?)")
            return serve()

    return serve()


@app.errorhandler(404)
def serve():
    return app.send_static_file('index.html')
