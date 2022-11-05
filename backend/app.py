from flask import Flask, render_template, send_file, request, abort, Response,redirect, url_for, flash, json, jsonify,send_from_directory, session
import urllib.request
import json
import configparser
import os
from os.path import join, dirname, realpath
import csv

app = Flask(__name__)
UPLOAD_FOLDER = './static/files/uploadedfiles'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER
filenames = []
jsonfilenames = []
app.secret_key = 'xyz'

@app.route('/forecastjson')
def forecastjson():
    with open('./static/files/response.json', 'r') as myfile:
        data = myfile.read()
        return render_template('forecastjson.html', title="page", jsonfile=json.dumps(data))


    
@app.route('/')
def home():
    jsonfilenames=(os.listdir('static/files/responsejson'))
    session['filenames'] = filenames
    return render_template('home.html',filenames=filenames, jsonfilenames=jsonfilenames)

@app.route('/download/<path:filename>', methods=['GET'])
def download():
    path = './static/files/responsejson/response.json'
    return send_file(path, as_attachment=True)

@app.route("/", methods=['POST'])
def uploadFiles():
      # get the uploaded file
    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
                print('No selected file')
                return redirect(url_for('home'))
        
    if uploaded_file.filename != '':
           uploaded_file.save(os.path.join(UPLOAD_FOLDER, uploaded_file.filename))
           filenames.append(uploaded_file.filename )
    parseCSV(os.path.join(UPLOAD_FOLDER, uploaded_file.filename))
    session['filenames'] = filenames
    jsonfilenames=(os.listdir('static/files/responsejson'))
    return render_template('home.html', filenames=filenames, jsonfilenames=jsonfilenames)

def parseCSV(filePath):
      
    file = open(filePath)
    type(file)
    
    with open(filePath, newline='') as infh:
        reader = csv.reader(infh)
        for row in reader:
            responsedata = getforecast(row[0])
            with open('./static/files/responsejson/response.csv', 'a', newline="") as file:
                csvwriter = csv.writer(file)
                csvwriter.writerow(responsedata)
    csv_to_json('./static/files/responsejson/response.csv', './static/files/responsejson/response.json')

# definition to convert the csv files to json format. 
def csv_to_json(csvFilePath, jsonFilePath):
    jsonArray = []
      
    #read csv file
    with open(csvFilePath, encoding='utf-8') as csvf: 
        #load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvf) 

        #convert each csv row into python dict
        for row in csvReader: 
            #add this python dict to json array
            jsonArray.append(row)
  
    #convert python jsonArray to JSON String and write to file
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf: 
        jsonString = json.dumps(jsonArray, indent=4)
        jsonf.write(jsonString)

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
    data = urllib.request.urlopen(full_url)

    resp = Response(data)
    resp.status_code = 200
    return render_template('forecast.html', title='Weather App', data=json.loads(data.read().decode('utf8')))

if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)