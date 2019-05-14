.PHONY: clean demo dist setup
clean:
	find . -regex "\(.*__pycache__.*\|*.py[co]\)" -delete
	rm -rf dist/
	rm -rf *.egg-info
	rm MANIFEST

demo:
	python3 pts.py -d example -vvvv

dist:
	python3 setup.py sdist

