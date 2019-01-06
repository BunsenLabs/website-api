CONTAINER ?= www-api
IMAGE ?= blwwwapi
TAG ?= latest
CONTAINER_IMAGE ?= $(IMAGE):$(TAG)

start-container:
	docker run -dit --network=host --log-opt max-size=10m --log-opt max-file=1 --name $(CONTAINER) $(CONTAINER_IMAGE)

stop-container:
	-docker stop $(CONTAINER)

build-container:
	docker build --rm . -t $(CONTAINER_IMAGE)

remove-container: | stop-container
	-docker rm $(CONTAINER)

replace: | build-container remove-container start-container

.PHONY: start-container stop-container build-container remove-container replace
