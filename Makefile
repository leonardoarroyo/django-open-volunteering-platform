test:
	@python ovp_news/tests/runtests.py

lint:
	@pylint ovp_news

clean-pycache:
	@rm -r **/__pycache__

clean: clean-pycache

.PHONY: clean


