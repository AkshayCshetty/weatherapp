# README #


### How do I get set up? ###

* Make sure Docker is installed/ download and install docker from https://docs.docker.com/get-docker/
* git clone git clone https://akshay-shetty@bitbucket.org/akshay-shetty/kairi-project.git
* cd to the directory 
* run the following commands :
    docker compose build 
    docker compose up -d 
* App is available at http://127.0.0.1:5000
* to shut down the app : docker compose down 

Second Method to run Project 
#go to the backend folder of the app. 
cd backend 
docker build --tag app .  
docker run -d -p 5000:5000 app
to check container : docker ps 
to stop docker container:  docker stop "container name "

Sometime port 5000 is used by another app or process to kill it and free port 5000 run 
lsof -P | grep ':5000' | awk '{print $2}' | xargs kill -9




Technology stack 
1. pyhton3
2. flask ( python flask framework)
3. docker ( to containerize the application)
4.