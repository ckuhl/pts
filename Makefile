ENV=env
PYTHON=env/bin/python3
PIP=env/bin/pip


.PHONY: clean setup
clean:
	find . -regex "\(.*__pycache__.*\|*.py[co]\)" -delete

setup:
	test -d ${ENV} || virtualenv -p /usr/bin/python3 --no-site-packages ${ENV}
	${PIP} install --upgrade pip
	${PIP} install --upgrade setuptools
	${PIP} install -r requirements.txt

