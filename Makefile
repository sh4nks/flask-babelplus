.PHONY: test tox clean wheel upload docs

test:
	pytest

tox:
	@tox

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

format: ## Sorts the imports and reformats the code
	# sort imports / remove unused
	ruff check --fix --select I
	ruff check --fix
	# reformat
	ruff format

dist:
	uv build

upload:
	twine upload dist/{*.tar.gz,*.whl} --skip-existing

docs:
	$(MAKE) -C docs html
