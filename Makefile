setup:
	python3 -m venv .venv
	source .venv/bin/activate
	pip3 install -r pip-requirements.txt

run:
	chmod +x code/main.py
	python3 code/main.py

docker_build:
	docker build -t ghostvr/meross-prometheus-exporter .

docker_run:
	docker run ghostvr/meross-prometheus-exporter

docker_probe:
	docker run -i -t ghostvr/meross-prometheus-exporter /bin/bash
