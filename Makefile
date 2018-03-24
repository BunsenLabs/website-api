build:
	git fetch origin
	git reset --hard origin/master
	docker build --rm . -t blwwwapi:latest

start:
	docker run -dit --network host --restart unless-stopped --name www-api blwwwapi:latest

.PHONY: build start
