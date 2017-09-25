ENV=env
PYTHON=env/bin/python3
PIP=env/bin/pip

SCRIPT=test.py

.PHONY: clean setup
clean:
	find . -regex "\(.*__pycache__.*\|*.py[co]\)" -delete

run:
	${PYTHON} ${SCRIPT}

setup:
	test -d ${ENV} || virtualenv -p /usr/bin/python3.5 --no-site-packages ${ENV}
	${PIP} install --upgrade pip
	${PIP} install --upgrade setuptools
	${PIP} install -r requirements.txt

