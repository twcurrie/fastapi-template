#! /usr/bin/env sh
# This script is intended to simplify the setup of all the dependencies for the service.
# The specified overrides within the docker-compose file also expose all their ports to
# system ports on the developer's machine.

# Exit in case of error
set -e

# Setup debug docker-compose file with overrides.
export COMPOSE_FILE=docker-compose.yml:docker-compose.debug.yml
docker-compose config > docker-stack.yml

docker-compose -f docker-stack.yml build
docker-compose -f docker-stack.yml down -v --remove-orphans # Remove any possible orphaned containers left from an error
docker-compose -f docker-stack.yml up -