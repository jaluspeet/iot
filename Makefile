all: server client

server:
	python server/server.py

client:
	python client/app.py

docker:
	docker-compose up --build

.PHONY: all server client docker
