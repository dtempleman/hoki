TEST_DIRS := hoki scripts

lint:
	black --check $(TEST_DIRS)
	flake8 $(TEST_DIRS)

coverage:
	coverage erase
	coverage run --source hoki -m pytest tests --durations=10
	coverage report --include=hoki/*
	coverage html --fail-under=60

sim:
	docker compose run --rm app python scripts/run_sim.py

game:
	docker compose run --rm app python scripts/sim_game.py