# TEAM SAVA HOME ASSINGMENT

## Overview

Provide application to allow basic authorization user functions

## Solution architecture

### Backend

Consists of Django server running in Docker.

Django has one app called `custom_auth` since everything in the document points to user autorization management.

Local development is done by docker-compose and there is a build tool (`Makefile`) added for convenience of running commands

#### Models

Two models exists in the app:

1. AuthUser: modified Django user that has no username field and uses the email field as unique identifier
2. EmailToken: Token with relatioship with AuthUser model, that would hold an UUID. This UUID is used to build the url to which user has to go to get to the password reset form to change it's password.

#### Endpoints

Endpoints can be found in the Postman collection located in `docs` dir of the repository.
Alternativelly API documentation is listed on the server `/docs/` endpoint.

Brief overview:

    1) `/api/v1/auth-user/` - supports create, read and delete functionalities of user accounts

    2) `/api/v1/reset-token/` - generating and retrieving password reset token.

    3) `/api/v1/reset-password/` - POST to this method resets the user password

    4) `/api/v1/auth-token/` - POST with credentials generats JWT access/referesh token pair used for authentication

    5) `/api/v1/'auth-token/refresh/' - POST with JWT refresh token generates a new access token

#### Authentication

Authentication is done with JWT tokens.

`django-restframeworkd-simple-jwt` is 3rd party library that offers great support for quick implementation of these tokens and is used in the assignment.

#### Celery

Assignment requires that email suppose to be sent through which user will get password reset url link. Since sending emails is done via 3rd party service (SENDGRID), it's a good practice to use asynchornous tasks queuer and go-to solution is Celery.

Celery uses rabbitmq for backend and the results are stored in the database for possible analytics.

This way the user gets quick response and the background task take over the email sending job.
