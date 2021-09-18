typehint:
	pytype .

formatter:
	python -m black ./

sort_import:
	isort **/*.py

save_checklist: sort_import typehint formatter