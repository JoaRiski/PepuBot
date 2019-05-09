#!/bin/sh
docker build \
	--pull \
	--no-cache \
	-t docker.anders.fi/riski/pepubot/$IMAGE:latest \
	-t docker.anders.fi/riski/pepubot/$IMAGE:$CI_COMMIT_SHA \
	-f dockerfiles/$IMAGE.Dockerfile .

if [[ $CI_COMMIT_REF_NAME == "master" ]];
then
	docker push docker.anders.fi/riski/pepubot/$IMAGE:latest
	docker push docker.anders.fi/riski/pepubot/$IMAGE:$CI_COMMIT_SHA
fi
