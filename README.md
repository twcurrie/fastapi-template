![Our mascot](docs/mascot.jpeg)

# FastAPI Template Service

Python-based microservice built with :heart: on the [FastAPI](https://github.com/tiangolo/fastapi) framework. The intent of this repo is to provide a skeleton application that includes as much as possible that will be required for our services. 

- [So what's included?](#so-whats-included)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Makefile](#makefile)
- [Environment Setup](#environment-setup)
- [Running the App](#running-the-app)
- [Test](#test)
- [Documentation](#documentation)

## So what's included?

There is _a lot_ built in out of the box. 

* Automated Swagger documentation (and redoc!)
* SQLAlchemy ORM with a Postgres database 
* Generic CRUD implementation with example data models.
* Alembic-managed migrations
* Basic, configurable, [rate limiting](https://github.com/laurentS/slowapi) using Redis.
* Example external API provided using Wiremock
* New Relic and Sentry scaffolding
* PHI-protecting decorators and handlers 
* Semaphore configurations
* Static security checks and dependency vulnerability checks  
* Request id generating middleware (provides back to client in a header!)
* Basic security logging on 
* JSON-formatted log handler with ability to provide additional fields in different contexts.
* Example SumoLogic dashboard
* Health check endpoints  
* Generic SHA-based versioning setup, with endpoint to obtain version
* Dockerfile and docker-compose ready
* Static type analysis with [mypy](https://mypy.readthedocs.io/en/stable/)
* Linting and formatting of code upon commit

[comment]: <> (* JWT auth guards )
[comment]: <> (* [KodiakHQ]&#40;https://github.com/marketplace/kodiakhq&#41; integrations for automatic PR merging)

## Cloning the repo

This app will work out of the box, however, there are a few instances of `template` or `{{template}}` around the repo that should be changed per your service name.

## Prerequisites

You'll need a few things to get started.

### Required

* [Docker](https://docs.docker.com/get-docker/)
* [docker-compose](https://docs.docker.com/compose/install/)

## Installation

Technically, since everything can be run using docker, you don't need to install dependencies locally, but if your IDE of choices requires it then just run `poetry install` to install everything.

## Makefile

A `Makefile` has been added to this project to simplify interactions with the service and docker. You can view it as an entrypoint for everything you'll need to do in this repo. To view all documented commands run `make help`.

## Running the App

To simplify development and follow [12 Factor App factor 10](https://12factor.net/dev-prod-parity), everything is run inside a docker-compose context. The following commands will get things up and running in development mode with hot-reloading.  An `.env` file is provided in the repo in order to simplify start-up of the application and its dependencies and share the credentials.

## Test

Unit, integration and end-to-end tests have been provided in the repo.  These are differentiated by:
* Unit tests require no external dependency.
* Integration tests require at least one external dependency (Postgres, eg.). 
* End-to-end tests interact externally with the application, and are generally intended to test the system after it has been deployed (typically in a scaling environment).

They can be run with the following commands:
* Unit tests: `make test-unit`
* Integration tests: `make test-integration`
* End-to-end tests: `make test-e2e`


## Authorization

Currently, the application only supports Basic Authentication requests.  The credentials to connect to the application are loaded as environment variables (visible in `.env`)


[comment]: <> (To correctly test an endpoint, you will need to generate a JWT that will pass internal validation checks.)

[comment]: <> (`npm run generateJwt` or `make generate-jwt` will produce the test JWT.)

### Coverage

Coverage is currently at 92%!

``` bash
-------------------------------------------------------------------------------------
Name                                      Stmts   Miss Branch BrPart  Cover   Missing
-------------------------------------------------------------------------------------
app/app/api/deps.py                          39     25      0      0    36%   15, 19-24, 28-35, 39-45, 49-55
app/app/api/v0/api.py                         7      0      0      0   100%
app/app/api/v0/endpoints/example.py          29      0      0      0   100%
app/app/api/v0/endpoints/patient.py          33      0      6      0   100%
app/app/backend_pre_start.py                 21      0      0      0   100%
app/app/core/config.py                       53      0      6      0   100%
app/app/core/controls.py                      4      0      0      0   100%
app/app/core/environment.py                  16      0      0      0   100%
app/app/core/exceptions.py                   16      1      0      0    94%   25
app/app/core/external_auth.py                81      0     14      0   100%
app/app/core/handlers.py                     25      5      0      0    80%   20-27
app/app/core/health/checks.py                23      0      0      0   100%
app/app/core/health/route.py                 13      0      5      0   100%
app/app/core/logging/config.py                1      0      0      0   100%
app/app/core/logging/filter.py               13      3      6      2    63%   12, 17-18
app/app/core/logging/formatter.py             8      0      0      0   100%
app/app/core/logging/log.py                  45      0     14      0   100%
app/app/core/middleware/http.py              23      0      2      0   100%
app/app/core/monitoring/new_relic.py          0      0      0      0   100%
app/app/core/monitoring/sentry.py            33      2     30      6    87%   19, 24, 34->42, 43->61, 66->82, 83->26
app/app/core/monitoring/utils.py              3      0      0      0   100%
app/app/core/security.py                     12      0      2      0   100%
app/app/core/version.py                       4      0      0      0   100%
app/app/crud/base.py                         39      0      6      0   100%
app/app/crud/crud_patient.py                  8      0      0      0   100%
app/app/db/base_class.py                      9      0      2      0   100%
app/app/db/session.py                        16      0      4      0   100%
app/app/db/types/phi_column.py               58     11     22      5    75%   25-27, 41, 78, 86, 93-96, 106
app/app/domain/example_api.py                23      0      2      0   100%
app/app/main.py                              31      0      0      0   100%
app/app/models/patient.py                     8      0      0      0   100%
app/app/schemas/enums/types.py               15      0      8      0   100%
app/app/schemas/external/example_api.py       3      0      0      0   100%
app/app/schemas/patient.py                   25      0      2      0   100%
app/app/schemas/utils.py                      3      0      2      0   100%
-------------------------------------------------------------------------------------
TOTAL                                       761     68    135     13    92%
```


## Documentation

Once the service is started, you can visit the `/docs` route to view the Swagger API docs, or `/redocs` to view the Redocs version of the docs.

## Example modules

Two example endpoints are provided to demonstrate functionality:
* `/example` - Shows basic requests to an external API.
* `/patient` - Shows basic CRUD operations on an endpoint.