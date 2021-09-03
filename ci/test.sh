#! /usr/bin/env sh

# Exit in case of error
set -e

# Setup docker-compose file with overrides.
DOCKER_BUILDKIT=1 INSTALL_DEV=true BUILD_IMAGE=dev docker-compose config > docker-stack.yml

docker-compose -f docker-stack.yml build
docker-compose -f docker-stack.yml down -v --remove-orphans # Remove any possible orphaned containers left from an error
docker-compose -f docker-stack.yml up -d
docker-compose -f docker-stack.yml exec -T eligibility-service bash /app/run-tests.sh "$@"
docker-compose -f docker-stack.yml down -v --remove-orphans # Shut down all the services.
