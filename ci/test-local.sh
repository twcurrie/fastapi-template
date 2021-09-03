#! /usr/bin/env bash

# Exit in case of error
set -e

# Ensure dev dependencies installed
docker-compose down -v --remove-orphans # Remove any possible orphaned containers left from an error
INSTALL_DEV=true docker-compose --env-file=.test.env build
docker-compose --env-file=.test.env up -d
docker-compose exec -T eligibility-service bash /app/run-tests.sh "$@"
docker-compose down -v --remove-orphans # Shut down all the services.
