import epiCalendar
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():

    jsessionid = request.form.get('jsessionid')
    filename = request.form.get('filename')

    return render_template('index.html')
