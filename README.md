# meross-prometheus
Meross smart plug energy consumption - prometheus exporter

# Build & Run instructions
* Create venv
```
python3 -m venv .venv
```

* Activate venv
```
source .venv/bin/activate
```

* (First time) install requirements
```
pip3 install -r pip-requirements.txt
```

* Local test
```
python3 code/main.py
```

* Docker related commands: Check Makefile

* Before release: Remember to update CURRENT_TAG in Makefile!
