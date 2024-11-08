# Makefile

dependencies: ## Install development dependencies
	pip install -U pip-tools
	pip-sync django/requirements.txt

freeze:  ## Run pip-compile to lock all base dependencies
	cd django/ && pip freeze > requirements.in

dependencies-compile:  ## Run pip-compile to lock all base dependencies
	cd django/ && pip-compile requirements.in --verbose

test: ## Run tests
	cd django/ && python manage.py test --failfast manager authentication

test-coverage: clean ## Run tests with coverage
	cd django/ &&
	ENV=TEST coverage run --source=authentication,manager manage.py test
	coverage report
	coverage html
	@echo "HTML report available at: django/htmlcov/index.html"

clean: ## Clean local environment files
	( \
		cd django && \
		find . -name "*.pyc" -o -name "*.pyo" -o -name "__pycache__" | xargs rm -rf && \
		rm -f .coverage && \
		rm -rf htmlcov/ && \
		rm -rf docs/build/ \
	)

run: ## Run Project
	cd django && python manage.py runserver

makemigrations: ## Make migrations
	cd django && python manage.py makemigrations

migrate: ## Apply migrations
	cd django && python manage.py migrate

lint: ## Run code lint
	flake8 --show-source django/
	isort --check-only django/
	black --check django/ --line-length=79
	mypy django/

fix-python-import: ## Organize python imports
	isort .

format-all: ## Format code with black and isort
	black django/ --line-length=79
	isort django/

start-sqlite: ## Copy .env_sqlite, down and up containers
	@sudo cp ./.env_sqlite ./.env && sudo docker-compose -f docker-compose-sqlite.yml down --volumes --remove-orphans && sudo docker-compose -f docker-compose-sqlite.yml up

start-postgresql: ## Copy .env_postgresql, down and up containers
	@sudo cp ./.env_postgresql ./.env && sudo docker-compose -f docker-compose-postgresql.yml down --volumes --remove-orphans && sudo docker-compose -f docker-compose-postgresql.yml up

stopped-sqlite: ## Copy Down containers
	@sudo docker-compose -f docker-compose-postgresql.yml down

stopped-postgresql: ## Down and up containers
	@sudo docker-compose -f docker-compose-sqlite.yml down

