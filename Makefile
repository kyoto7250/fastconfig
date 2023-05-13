style:
	poetry run black fastconfig/ tests/
	poetry run isort fastconfig/ tests/
	poetry run ruff fastconfig/ tests/

test:
	poetry run  pytest --cov=fastconfig --cov-report=html
