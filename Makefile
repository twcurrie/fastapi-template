SERVICE_NAME := {{ template-service }}
ENVIRONMENT := ${ENVIRONMENT}
AWS_DEFAULT_REGION := us-east-1
ECR_REGISTRY := 711154312405.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${SERVICE_NAME}
GIT_SHA := $$(git rev-parse --short HEAD)

# Login to aptible with bot account
aptible-login:
	@ aptible login --email=${APTIBLE_ROBOT_EMAIL} --password=${APTIBLE_ROBOT_PASSWORD} --lifetime='1hr'

# Deploy to aptible by pulling image from private docker registry
aptible-deploy:
	aptible deploy --git-detach \
		--app=${SERVICE_NAME}-${ENVIRONMENT} \
		--environment=${ENVIRONMENT} \
		--docker-image=$(ECR_REGISTRY):${GIT_SHA} \
		--private-registry-username=AWS \
		--private-registry-password=`aws ecr get-login-password --region us-east-1`

# Post deployment to New Relic endpoint
notify-new-relic-of-deploy:
	curl -X POST "https://api.newrelic.com/v2/applications/${NEW_RELIC_APP_ID}/deployments.json" \
     -H "X-Api-Key:${NEW_RELIC_API_KEY}" -i \
     -H 'Content-Type: application/json' \
     -d \ "`git log -1 --pretty=format:'{"deployment": {"revision":"%h","description":"%s", "user":"%an"}}' | cat`"

# Login to AWS registry (must have docker running)
ecr-login:
	aws ecr get-login-password --region ${AWS_DEFAULT_REGION} | docker login -u AWS --password-stdin ${ECR_REGISTRY}

# Build docker target, use
docker-build:
	sh ci/read_version.sh > version.json
	docker build -f Dockerfile --build-arg BUILDKIT_INLINE_CACHE=1 --no-cache -t ${SERVICE_NAME} .

# Push to registry
docker-push:
	docker push $(ECR_REGISTRY):${GIT_SHA}

# Tag docker image
docker-tag:
	docker tag ${SERVICE_NAME} $(ECR_REGISTRY):${GIT_SHA}

# Remove current latest image from container registry, then update with newest (to run after master merge)
docker-tag-latest:
	aws ecr batch-delete-image --region ${AWS_DEFAULT_REGION}  --repository-name ${SERVICE_NAME} --image-ids imageTag=latest; \
	docker tag ${SERVICE_NAME} $(ECR_REGISTRY):latest; \
	docker push $(ECR_REGISTRY):latest;

# Run unit tests
test-unit:
	poetry run pytest -m unit
