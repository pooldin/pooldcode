# Magical make incantations...
.DEFAULT_GOAL := deps

.PHONY: clean deps run run-test


clean:
	find . -name "*.py[co]" -exec rm -rf {} \;
	rm -rf build dist

deps:
	@python setup.py develop

run:
	@foreman start -f dev/Procfile

run-test:
	@foreman start
