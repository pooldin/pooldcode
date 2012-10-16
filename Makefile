# Magical make incantations...
.DEFAULT_GOAL := deps

.PHONY: clean deps dist run run-test upload upload-dev upload-nightly \
		upload-release


RUN=foreman run
SETUP=$(RUN) python setup.py
REV=$(shell git rev-parse --short HEAD)
TIMESTAMP=$(shell date +'%s')


build: clean
	@$(SETUP) build

clean:
	@find . -name "*.py[co]" -exec rm -rf {} \;
	@$(SETUP) clean
	@rm -rf dist build *.egg-info

deps:
	@$(SETUP) develop

dist: clean
	@$(SETUP) sdist

run:
	@foreman start -f dev/Procfile

run-test:
	@foreman start

upload: upload-dev

upload-dev: clean
	@$(SETUP) egg_info --tag-build='-dev.$(TIMESTAMP).$(REV)' sdist upload -r pooldin

upload-nightly: clean
	@$(SETUP) egg_info --tag-date --tag-build='-dev' sdist upload -r pooldin

upload-release: clean
	@$(SETUP) sdist upload -r pooldin
