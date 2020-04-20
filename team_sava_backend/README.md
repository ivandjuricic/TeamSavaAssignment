# team_sava_backend

Run the server

```
make build
make db
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
