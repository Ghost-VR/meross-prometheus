DOCKER_IMAGE_NAME = ghostvr/meross-prometheus-exporter
PLATFORM = linux/arm64,linux/amd64

setup:
	python3 -m venv .venv
	source .venv/bin/activate
	pip3 install -r pip-requirements.txt

run:
	chmod +x code/main.py
	python3 code/main.py

docker_build:
	docker build --platform $(PLATFORM) -t $(DOCKER_IMAGE_NAME) .

docker_run:
	docker run $(DOCKER_IMAGE_NAME)

docker_probe:
	docker run -i -t $(DOCKER_IMAGE_NAME) /bin/bash

docker_push:
	docker push $(DOCKER_IMAGE_NAME):latest
