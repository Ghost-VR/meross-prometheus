setup:
	python3 -m venv .venv
	source .venv/bin/activate
	pip3 install -r pip-requirements.txt

run:
	chmod +x code/main.py
	python3 code/main.py
