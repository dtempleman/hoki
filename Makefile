lint:
	./utils/lint.sh

coverage:
	coverage erase
	coverage run --source hoki -m pytest tests --durations=10
	coverage report --include=hoki/*
	coverage html --fail-under=60
