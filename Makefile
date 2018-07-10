build:
	docker build --rm . -t blwwwapi:latest

start:
	docker run -dit --network host --restart unless-stopped --name www-api blwwwapi:latest

replace: build
	docker stop www-api
	docker rm www-api
	docker run -dit --network host --restart unless-stopped --name www-api blwwwapi:latest

.PHONY: build start
