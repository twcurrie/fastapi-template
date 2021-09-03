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

Coverage is currently at 100%!

``` bash
-------------------------------------|---------|----------|---------|---------|-------------------
File                                 | % Stmts | % Branch | % Funcs | % Lines | Uncovered Line #s
-------------------------------------|---------|----------|---------|---------|-------------------
All files                            |     100 |      100 |     100 |     100 |
 src                                 |     100 |      100 |     100 |     100 |
  app.controller.ts                  |     100 |      100 |     100 |     100 |
 src/filters                         |     100 |      100 |     100 |     100 |
  sentry.filter.ts                   |     100 |      100 |     100 |     100 |
  unauthorized-exception.filter.ts   |     100 |      100 |     100 |     100 |
 src/hinge-jwt                       |     100 |      100 |     100 |     100 |
  index.ts                           |     100 |      100 |     100 |     100 |
  invalid-hinge-jwt-payload-error.ts |     100 |      100 |     100 |     100 |
  issuer.ts                          |     100 |      100 |     100 |     100 |
  types.ts                           |     100 |      100 |     100 |     100 |
  validator.ts                       |     100 |      100 |     100 |     100 |
 src/middleware                      |     100 |      100 |     100 |     100 |
  http-guard.middleware.ts           |     100 |      100 |     100 |     100 |
 src/middleware/rate-limiter         |     100 |      100 |     100 |     100 |
  index.ts                           |     100 |      100 |     100 |     100 |
  rate-limiter.ts                    |     100 |      100 |     100 |     100 |
  too-many-requests-exception.ts     |     100 |      100 |     100 |     100 |
 src/modules/auth                    |     100 |      100 |     100 |     100 |
  jwt-auth.guard.ts                  |     100 |      100 |     100 |     100 |
 src/modules/health                  |     100 |      100 |     100 |     100 |
  health.controller.ts               |     100 |      100 |     100 |     100 |
 src/security-logger                 |     100 |      100 |     100 |     100 |
  security-logger.service.ts         |     100 |      100 |     100 |     100 |
-------------------------------------|---------|----------|---------|---------|-------------------

Test Suites: 9 passed, 9 total
Tests:       24 passed, 24 total
Snapshots:   0 total
Time:        6.139s
Ran all test suites.
✨  Done in 7.01s.

```


## Documentation

Once the service is started, you can visit the `/docs` route to view the Swagger API docs, or `/redocs` to view the Redocs version of the docs.

## Example modules

Two example endpoints are provided to demonstrate functionality:
* `/example` - 
* `/patient` - 