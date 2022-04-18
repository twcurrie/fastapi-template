
![Our mascot](docs/mascot.jpeg)

# FastAPI Template Service
![badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/twcurrie/8258585e21c308f94b8ba0d66aefe1d0/raw/result.json)


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

## Documentation

Once the service is started, you can visit the `/docs` route to view the Swagger API docs, or `/redocs` to view the Redocs version of the docs.

## Example modules

Two example endpoints are provided to demonstrate functionality:
* `/example` - Shows basic requests to an external API.
* `/patient` - Shows basic CRUD operations on an endpoint.
