# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* Quick summary
* Version
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### How do I get set up? ###

* Summary of set up
* Configuration
* Dependencies
* Database configuration
* How to run tests
* Deployment instructions

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact



@app.route('/forecast', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if city is None:
        abort(400, 'Missing argument city')
    data = {}
    data['q'] = request.args.get('city')
    data['appid'] = 'b9b5716dbc568a9932c856ce9a9e98df'
    data['units'] = 'metric'

    url_values = urllib.parse.urlencode(data)
    url = 'http://api.openweathermap.org/data/2.5/forecast'
    full_url = url + '?' + url_values
    data = urllib.request.urlopen(full_url)

    resp = Response(data)
    resp.status_code = 200
    return render_template('index.html', title='Weather App', data=json.loads(data.read().decode('utf8')))

if __name__ == '__main__':
	app.run()


    city = request.form['city']