# team_sava_backend

## This is a template for new project when using django-admin command

Example of usage:

`django-admin startproject MYNEWPROJECT --template=https://github.com/ivandjuricic/docker-django-project-template/archive/master.zip --extension=py,md,ini,yml --name=Dockerfile,.env`

The command above will create new project under provided path (if no path provided directory will be create with the project name).

Simple

```
make migrate
make runserver
```

will start the development server.

To access the admin portal, run `make createsuperuser` and the command line will guide you through creation of user with admin privileges

Alternatively, Makefile is added to templates with provided commands:

- `build`
- `runserver`
- `bash` - runs bash inside of the docker
- `migrations` - creates migration
- `migrate` - applies migration to database
- `createsuperuser`
- `createuser`
- `static` - collectstatic management command
- `messages` - makemessages command
- `translation` - compilemessages management command
- `shell`
- `test`
- `teardown`
