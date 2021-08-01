# Proof of Concept Using a Sample Service (A Microservice)

That stores and handle any activity that involves operators

This service was built to proof the concept of having workers help move data between to database in the background.
With NoSql databases performing faster during query, I decided to build a system that queries data from a No sql database like Mongodb but then writes directly into a SQL database. This would reduce the amount of calls to each database. Especially in a high traffic website that entertains huge volume of traffic that either queries or creates data. 

When a user is to be created, it writes into the SQL db, and within a minute(This can be customized to whatever time interval) it then performs a mass write operations into the NoSQL database in one connection. You might be concerned that if within a minute the user that was created, quries his information?? This is were a cache db like redis would be used to return the data that was captured on creation.

If a minor update is done on the NoSQL (like an update of status or pin), the SQL would get those changes by noon every night. MEaning a worker would be assigned to update the SQL database also.


### Workers

No worker was killed during the developemnt of this :) 
- A worker to Update the NoSQL database in a minute
- A worker to update the SQL every Midnight

## Note Before Building Images OR Runing Locally
- In both .env file replace <AUTH_TOKEN> with an actual Authentication Token from Twillo , along with with an Account Sid
- Also remember to change the database password and name.
- Insert Actual Private and Public Key into both .env file


## To Run Locally 

set it up
------

Create a virtual environment and install the requirements

    $ python3 -m venv ./venv
    $ source ./venv/bin/activate
    $ pip install -r requirements.txt


Get the local database ready

    $ python init_db.py

Start the development server

    $ FLASK_APP=wsgi.py flask run
    * Serving Flask app "wsgi.py"
    * Environment: production
    WARNING: Do not use the development server in a production environment.
    Use a production WSGI server instead.
    * Debug mode: off
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit

Check the service at http://127.0.0.1:5000/


Tests
------

Run the unit tests with, Typically this is required, but for this module it is not required.

    $ pytest


Dependencies
------

MessageBackend uses Flask as a web framework, Flask RESTplus for creating the interface, and SQLAlchemy to handle the database models. It uses a SQLlite database for local development. It uses Celery to handle Asynchronous Task, while Rabbit Mq is used as a message broker.

- NoSQL Database -  MONGODB
- SQL Database - POSTGRES

Background Processses 
------

Ensure that the message broker Rabbit MQ is running in the background,if its not

    *$ Start the Rabbit MQ service
 
Start a Celery process in the bacground by running

    *$ celery worker -A celery_worker.celery --loglevel=info

start a celery beat in the background also

    *$ celery beat -A celery_worker.celery --loglevel=info

## To Run As Services

Run the docker-compose instance:

    *$ docker-compose up

#### Note
If you changed your details in your enviroment files, make sure to update your *docker-compose.yaml* and the DockerFiles accordingly.
