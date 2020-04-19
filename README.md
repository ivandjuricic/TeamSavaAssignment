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

1. `cp .env.template .env` - this will hold up some of the secrets. Change the STRIPE_API_KEY to the api key provided in the separate document
2. run `make db` to initialize the database and wait a few seconds
3. run `make migrate` to apply djanog app migrations to the database
4. run `make runserver` to start backend application

#### Models

Two models exists in the app:

1. AuthUser: modified Django user that has no username field and uses the email field as unique identifier
2. EmailToken: Token with relatioship with AuthUser model, that would hold an UUID. This UUID is used to build the url to which user has to go to get to the password reset form to change it's password.

#### Endpoints

Endpoints can be found in the Postman collection located in `docs` dir of the repository.

Brief overview:

    1) `/api/v1/auth-user/` - supports create, read and delete functionalities of user accounts

    2) `/api/v1/reset-token/` - generating and retrieving password reset token.

    3) `/api/v1/reset-password/` - POST to this method resets the user password

    4) `/api/v1/auth-token/` - POST with credentials generats JWT access/referesh token pair used for authentication

    5) `/api/v1/auth-token/refresh/' - POST with JWT refresh token generates a new access token

#### Authentication

Authentication is done with JWT tokens.

`django-restframeworkd-simple-jwt` is 3rd party library that offers great support for quick implementation of these tokens and is used in the assignment.

#### Celery

Assignment requires that email suppose to be sent through which user will get password reset url link. Since sending emails is done via 3rd party service (SENDGRID), it's a good practice to use asynchornous tasks queuer and go-to solution is Celery.

Celery uses rabbitmq for backend and the results are stored in the database for possible analytics.

This way the user gets quick response and the background task take over the email sending job.

#### Testing

Tests are included for the backend part of the assignment.

To run tests execute:
`make test`

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
