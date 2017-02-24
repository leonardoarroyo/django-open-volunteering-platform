test:
	@python ovp_uploads/tests/runtests.py

lint:
	@pylint ovp_uploads

clean-pycache:
	@rm -r **/__pycache__

clean: clean-pycache

.PHONY: clean


