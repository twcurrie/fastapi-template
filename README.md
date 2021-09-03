![Our mascot](docs/mascot.jpeg)

# FastAPI Template Service

Python JWT based authentication microservice built with :heart: on the [FastAPI](https://github.com/tiangolo/fastapi) framework. The intent of this repo is to provide a skeleton application that includes as much as possible that will be required for our services. 

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

* Automated Swagger documentation
* SQLAlchemy ORM with a Postgres database
* Alembic-managed migrations
* Basic, configurable, [rate limiting](https://github.com/laurentS/slowapi) using Redis.
* New Relic and Sentry scaffolding
* PHI-protecting decorators and handlers 
* Semaphore configurations
* Basic security logging
* JSON-formatted log handler
* Example SumoLogic dashboard
* Dockerfile and docker-compose ready
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

To simplify development and follow [12 Factor App factor 10](https://12factor.net/dev-prod-parity), everything is run inside a docker-compose context. The following commands will get things up and running in development mode with hot-reloading.  An `.sample.env` file is provided in the repo in order to simplify start-up of the application and its dependencies and share the credentials.

## Test

Unit, integration and end-to-end tests have been provided in the repo.  

[comment]: <> (* Unit tests: `make test`)

[comment]: <> (* E2E tests: `make test-e2e`. Note: you must run `make start` for these to run as they run inside the container.)

## Authorization

Currently, the application only supports Basic Authentication requests.  The


[comment]: <> (To correctly test an endpoint, you will need to generate a JWT that will pass internal validation checks.)

[comment]: <> (`npm run generateJwt` or `make generate-jwt` will produce the test JWT.)

### Coverage

Coverage is currently at 92%!

``` bash
-------------------------------------------------------------------------------------
Name                                      Stmts   Miss Branch BrPart  Cover   Missing
-------------------------------------------------------------------------------------
app/app/__init__.py                          12      0      0      0   100%
app/app/api/__init__.py                       0      0      0      0   100%
app/app/api/deps.py                          25     17      0      0    32%   10-15, 19-25, 29-35
app/app/api/v0/__init__.py                    0      0      0      0   100%
app/app/api/v0/api.py                         7      0      0      0   100%
app/app/api/v0/endpoints/__init__.py          0      0      0      0   100%
app/app/api/v0/endpoints/example.py          29      0      0      0   100%
app/app/api/v0/endpoints/patient.py          33      0      6      0   100%
app/app/backend_pre_start.py                 21      0      0      0   100%
app/app/core/__init__.py                      0      0      0      0   100%
app/app/core/config.py                       53      0      6      0   100%
app/app/core/controls.py                      4      0      0      0   100%
app/app/core/environment.py                  16      0      0      0   100%
app/app/core/exceptions.py                   16      1      0      0    94%   25
app/app/core/external_auth.py                81      6     14      1    91%   144-154
app/app/core/handlers.py                     25      5      0      0    80%   20-27
app/app/core/health/__init__.py               0      0      0      0   100%
app/app/core/health/checks.py                23      0      0      0   100%
app/app/core/health/route.py                 13      0      5      0   100%
app/app/core/logging/__init__.py              7      0      0      0   100%
app/app/core/logging/config.py                1      0      0      0   100%
app/app/core/logging/filter.py               13      3      6      2    63%   12, 17-18
app/app/core/logging/formatter.py             8      0      0      0   100%
app/app/core/logging/log.py                  47      1     16      1    97%   62
app/app/core/middleware.py                   23      0      2      0   100%
app/app/core/monitoring/__init__.py           2      0      0      0   100%
app/app/core/monitoring/new_relic.py          0      0      0      0   100%
app/app/core/monitoring/sentry.py            33      2     30      6    87%   19, 24, 34->42, 43->61, 66->82, 83->26
app/app/core/monitoring/utils.py              3      0      0      0   100%
app/app/core/security.py                     12      0      2      0   100%
app/app/core/version.py                       4      0      0      0   100%
app/app/crud/__init__.py                      3      0      0      0   100%
app/app/crud/base.py                         39      0      6      0   100%
app/app/crud/crud_patient.py                  8      0      0      0   100%
app/app/db/__init__.py                        0      0      0      0   100%
app/app/db/base_class.py                      9      0      2      0   100%
app/app/db/session.py                        16      0      4      0   100%
app/app/db/types/__init__.py                  0      0      0      0   100%
app/app/db/types/phi_column.py               58     11     22      5    75%   25-27, 41, 78, 86, 93-96, 106
app/app/domain/example_api.py                23      0      2      0   100%
app/app/main.py                              31      0      0      0   100%
app/app/models/__init__.py                    0      0      0      0   100%
app/app/models/patient.py                     8      0      0      0   100%
app/app/schemas/__init__.py                   1      0      0      0   100%
app/app/schemas/enums/__init__.py             0      0      0      0   100%
app/app/schemas/enums/types.py               15      0      8      0   100%
app/app/schemas/external/__init__.py          0      0      0      0   100%
app/app/schemas/external/example_api.py       3      0      0      0   100%
app/app/schemas/patient.py                   25      0      2      0   100%
app/app/schemas/utils.py                      3      0      2      0   100%
-------------------------------------------------------------------------------------
TOTAL                                       753     46    135     15    92%

```


## Documentation

Once the service is started, you can visit the `/docs` route to view the Swagger API docs, or `/redocs` to view the Redocs version of the docs.

## Example modules

Two example endpoints are provided to demonstrate functionality:
* `/example` - 
* `/patient` - 