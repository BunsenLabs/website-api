build:
	docker build --rm . -t blwwwapi:latest

start:
	docker run -dit --network=host --name www-api blwwwapi:latest

replace: build
	docker stop www-api
	docker rm www-api
	docker run -dit --name www-api blwwwapi:latest

stop:
	docker stop www-api

.PHONY: build start
