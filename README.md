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
webpage is availabe at http://127.0.0.1:5000
install DOCKER https://docs.docker.com/get-docker/

if you wnat to run the docker solution.
#go to the backend folder of the app. 
cd backend 
docker build --tag app .  
docker run -d -p 5000:5000 app
to check container : docker ps 
to stop docker container:  docker stop "container name "


if you wnat to run python solution 
cd backend
python3 -m venv venv 
source venv/bin/activate   
pip3 install Flask  
export FLASK_APP=app.py  
flask run 
or
python3 app.py
ctr + c to kill the app 