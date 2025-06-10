# https://www.client9.com/self-documenting-makefiles/
.PHONY: help
help:
	@awk -F ':|##' '/^[^\t].+?:.*?##/ {\
	printf "\033[36m%-32s\033[0m %s\n", $$1, $$NF \
	}' $(MAKEFILE_LIST)

HOST?=0.0.0.0
PORT?=8001
run: ## Run the server, set HOST or PORT
	flask --app server.py run --host ${HOST} --port ${PORT}

requirements: ## Install requirements via pip
	pip install -r requirements.txt
