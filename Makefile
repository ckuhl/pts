ENV=env
PYTHON=env/bin/python3
PIP=env/bin/pip

SCRIPT=pts.py


.PHONY: clean demo dist setup
clean:
	find . -regex "\(.*__pycache__.*\|*.py[co]\)" -delete
	rm -rf dist/
	rm -rf *.egg-info
	rm MANIFEST

demo:
	${PYTHON} ${SCRIPT} -d example -vvvv

dist:
	${PYTHON} setup.py sdist

setup:
	test -d ${ENV} || virtualenv -p /usr/bin/python3.5 --no-site-packages ${ENV}
	${PIP} install --upgrade pip
	${PIP} install --upgrade setuptools
	${PIP} install -r requirements.txt

