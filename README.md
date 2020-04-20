# TEAM SAVA HOME ASSINGMENT

## Overview

Provide application to allow basic authorization user functions

## Solution architecture

### Backend

Consists of Django server running in Docker. Database, Celery workers and RabbitMQ also dockerised and Docker-compose is used for orchestration.

Django server has one app called `custom_auth` since everything in the document points to user autorization management.

Local development is done by docker-compose and there is a build tool (`Makefile`) added for convenience of running commands

#### Installation

After cloning the repo and navigating to:

`TeamSavaAssignment/team_sava_backend`

1. `cp .env.template .env` - this will hold up some of the secrets. Change the STRIPE_API_KEY to the api key provided in the separate document (this could be done in process of docker build but I this approach as it is more explicit)
2. run `make build` to build the dockers and install python dependencies
3. run `make db` to initialize the database and wait a few seconds
4. run `make migrate` to apply djanog app migrations to the database
5. run `make runserver` to start backend application and wait until all containers are up and running

#### Authentication

Authentication is done with JWT tokens.

`django-restframeworkd-simple-jwt` is 3rd party library that offers great support for quick implementation of these tokens and is used in the assignment.

### Documentation

API and Models documentation are available on 

* `/docs/` endpoint for Swagger documentation
* `/redoc` endpoin for Redoc documentation

Alternatively there is Postman collection export in the `team_sava_backend/docs/TeamSava.postman_collection.json` file

#### Celery

Assignment requires that email suppose to be sent through which user will get password reset url link. Since sending emails is done via 3rd party service (SENDGRID), it's a good practice to use asynchornous tasks queuer and go-to solution is Celery.

Celery uses rabbitmq for backend and the results are stored in the database for possible analytics.

This way the user gets quick response and the background task take over the email sending job.

#### Testing

Tests are included for the backend part of the assignment.

To run tests execute:
`make test`

#### Logging

Logs for django request erros are in the `team_sava_backend/team_sava_backend/logs/errors.log` file
Logs for celery tasks are in the `team_sava_backend/team_sava_backend/logs/celery.log` file

Other logging handlers could be used but file logs are easy to push and monitor with ELK stack and Filebeat

### Frontend

Frontend is simple create-react-app application made only for purposes of calling the api and checking it's results.

This application should be created in a separate repository, but since this was out of scope for assignment leaving it in the same one.

Many features lack this application. Some more noticablea are: form validations, surfacing to the forms backend 400s, since this is a python challenge felt that this is out of scope too.

#### Installation

In a different terminal from the backend server navigate to:
`TeamSavaAssignment/team_sava_frontend`

and run:

1. cp `.env.template .env`
2. `npm install`
3. `npm start`
4. profit



# TROUBLESHOOTING

1) ### Password reset email not being sent:

If everything works but the email is not sending it is possible that the Sendgrid credentials are not populated

Check if there is a `.env` file and that the `SENDGRID_API_KEY` is not __CHANGEME__

2) ### URL in the email is not working

Make sure that Django settings has DOMAIN variable that points to the correct frontend server.
By default it should be http://localhost:3000 but if local setup is different this should be changed


3) ### Server running but no responses from server
   
When using frontend make sure there is a `.env` file has correct `REACT_APP_BACKEND_HOST` pointing to backend server.

By default it should be http://localhost:8000 but if local setup is different this should be changed