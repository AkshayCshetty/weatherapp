from flask import Flask, render_template, abort, send_file, request, abort, Response,redirect, url_for, flash, json, jsonify,send_from_directory, session
import urllib.request
import json
import configparser
import os
from os.path import join, dirname, realpath
import csv
from urllib.error import HTTPError

app = Flask(__name__)
UPLOAD_FOLDER = './static/files/uploadedfiles'
DOWNLOAD_FOLDER = './static/files/responsejson'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER
filenames = []
jsonfilenames = []
formatjson = 'json'
app.secret_key = 'xyz'

@app.route('/')
def home():
    jsonfilenames=(os.listdir(DOWNLOAD_FOLDER))
    filenames=(os.listdir(UPLOAD_FOLDER))
    session['jsonfilenames'] = jsonfilenames
    session['filenames'] = filenames
    return render_template('home.html',filenames=filenames,jsonfilenames=jsonfilenames)

@app.route("/", methods=['POST'])
def uploadFiles():
      # get the uploaded file
    
    uploaded_file = request.files['file']
                  
    if uploaded_file.filename != '':
           uploaded_file.save(os.path.join(UPLOAD_FOLDER, uploaded_file.filename))
           filenames.append(uploaded_file.filename )
    parseCSV(os.path.join(UPLOAD_FOLDER, uploaded_file.filename))
    jsonfilenames=(os.listdir(DOWNLOAD_FOLDER))
    
    session['filenames'] = filenames
    session['jsonfilenames'] = jsonfilenames
    return render_template('home.html', filenames=filenames, jsonfilenames=jsonfilenames)

@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    full_path = os.path.join(app.root_path, UPLOAD_FOLDER)
    return send_from_directory(full_path, filename, as_attachment=True)

@app.route('/downloadjosn/<path:filename>', methods=['GET'])
def downloadjosn(filename):
    full_path = os.path.join(app.root_path, DOWNLOAD_FOLDER)
    return send_from_directory(full_path, filename, as_attachment=True)

def getforecast(city):
    
    if city is not None:
        data = {}
        data['q'] = city
        # this is the app id from openweather, currently in my id, should change when a new user is using. 
        data['appid'] = 'b9b5716dbc568a9932c856ce9a9e98df'
        data['units'] = 'metric'

        url_values = urllib.parse.urlencode(data)
        url = 'http://api.openweathermap.org/data/2.5/forecast'
        full_url = url + '?' + url_values
        data = urllib.request.urlopen(full_url)
        return data   

@app.route('/forecast',  methods=['POST', 'GET'])
def forecast():
    data = {}
    if request.method == 'POST':
        city = request.form['city']
    else: 
        city = request.args.get('city') 
    if city is None:
        abort(400, 'Missing argument city')
    data['q'] = city
    data['appid'] = 'b9b5716dbc568a9932c856ce9a9e98df' # this is the app id from openweather, currently in my id, should change when a new user is using. 
    data['units'] = 'metric'

    url_values = urllib.parse.urlencode(data)
    url = 'http://api.openweathermap.org/data/2.5/forecast'
    full_url = url + '?' + url_values

    try:
        data = urllib.request.urlopen(full_url)
    except HTTPError as err:
        if err.code == 404:
            return render_template('error.html')
    responsestring = data.read().decode('utf-8')
    json_obj = json.loads(responsestring)
    response_file_city=os.path.join(DOWNLOAD_FOLDER, city+'.'+formatjson)
    with open(response_file_city, 'w', newline="") as file:
        file.write(json.dumps(json_obj,indent=4))
    resp = Response(data)
    resp.status_code = 200
    return render_template('forecast.html', title='Weather App', data=json_obj)
    

# not required function as we are providing files to download. 
@app.route('/forecastjson')
def forecastjson():
    with open('./static/files/response.json', 'r') as myfile:
        data = myfile.read()
        return render_template('forecastjson.html', title="page", jsonfile=json.dumps(data))


def parseCSV(filePath):
      
    file = open(filePath)
    type(file)
    
    with open(filePath, newline='') as infh:
        reader = csv.reader(infh)
        full_path = os.path.join(app.root_path, DOWNLOAD_FOLDER)
        for row in reader:
            responsedata = getforecast(row[0])
            json_obj_m = Response(responsedata)
            responsestring = responsedata.read().decode('utf-8')
            json_obj = json.loads(responsestring)
            result_final=json_obj.pop('list')
            result_final.append(json_obj.pop('city'))
            
            response_file_city=os.path.join(DOWNLOAD_FOLDER, row[0]+'.'+formatjson)
            with open(response_file_city, 'w', newline="") as file:
                file.write(json.dumps(result_final, indent=4))    
                
if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)