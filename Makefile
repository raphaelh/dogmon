SHELL = /bin/bash
BOLD  = \033[1m
DIM   = \033[2m
RED   = \033[31m
RESET = \033[0m

# Use the activated venv path or use "venv"
VENV_DIR  := $(shell echo $${VIRTUAL_ENV-venv})
# Used to store make stamps
STAMP_DIR := $(VENV_DIR)

SOURCES   := $(wildcard src/dogmon/*.py)
TESTS     := $(wildcard tests/*.py)

# Check python3 version is greater than or equal to 3.6
#function check_python_version {
#    version=$(python3 -V | cut -d\  -f 2)
#    version=(${version//./ })#

#    if [[ ${version[0]} -lt 3 ]] || [[ ${version[0]} -eq 3 && ${version[1]} -lt 6 ]] ; then
#        echo >&2 "Python 3.6+ is required to run this project!"
#        exit 1
#    fi
#}


venv: $(STAMP_DIR)/.venv-stamp ## Create the venv
$(STAMP_DIR)/.venv-stamp: setup.py
	@echo -e "$(BOLD)Creating the venv$(RESET)"
	@echo -e -n "$(DIM)"
	@test -d $(VENV_DIR) || python3 -m venv $(VENV_DIR)
	@ . $(VENV_DIR)/bin/activate
	@touch $@
	@echo -e -n "$(RESET)"
	@echo -e "Don't forget to run $(BOLD). $(VENV_DIR)/bin/activate$(RESET) before working on the project :)"
	
install: $(STAMP_DIR)/.install-stamp ## Install dogmon in the venv
$(STAMP_DIR)/.install-stamp: $(SOURCES) $(STAMP_DIR)/.venv-stamp
	@echo -e "$(BOLD)Installing dogmon in the venv$(RESET)"
	@echo -e -n "$(DIM)"
	@ . $(VENV_DIR)/bin/activate ;\
	python -m pip install -U pip ;\
	python -m pip install -U .
	@touch $@
	@echo -e -n "$(RESET)"

install-dev: $(STAMP_DIR)/.install-dev-stamp ## Install dogmon in the venv with dev requirements
$(STAMP_DIR)/.install-dev-stamp: $(SOURCES) $(STAMP_DIR)/.venv-stamp
	@echo -e "$(BOLD)Installing dogmon in the venv with dev requirements$(RESET)"
	@echo -e -n "$(DIM)"
	@ . $(VENV_DIR)/bin/activate ;\
	python -m pip install -U pip ;\
	python -m pip install -U -e .[dev]
	@touch $@
	@echo -e -n "$(RESET)"

lint: $(STAMP_DIR)/.lint-stamp ## Run code checks
$(STAMP_DIR)/.lint-stamp: $(STAMP_DIR)/.install-dev-stamp
	@echo -e "$(BOLD)Running code checks$(RESET)"
	@echo -e -n "$(DIM)"
	@ . $(VENV_DIR)/bin/activate ;\
	flake8 $^
	@touch $@
	@echo -e -n "$(RESET)"
	
test: $(STAMP_DIR)/.test-stamp ## Run all the tests
$(STAMP_DIR)/.test-stamp: $(TESTS) $(STAMP_DIR)/.venv-stamp
	@echo -e "$(BOLD)Running all the tests$(RESET)"
	@echo -e -n "$(DIM)"
	@ . $(VENV_DIR)/bin/activate ;\
	pytest --verbose --color=yes $(TESTS)
	@touch $@
	@echo -e -n "$(RESET)"
	
ci: lint test ## Run all the tests and code checks

dist: $(STAMP_DIR)/.dist-stamp ## Build a wheel with dogmon
$(STAMP_DIR)/.dist-stamp: $(STAMP_DIR)/.install-dev-stamp
	@echo -e "$(BOLD)Building a wheel with dogmon$(RESET)"
	@echo -e -n "$(DIM)"
	@ . $(VENV_DIR)/bin/activate ;\
	python setup.py bdist_wheel
	@touch $@
	@echo -e -n "$(RESET)"

run: install ## Run dogmon in the venv
	@echo -e "$(BOLD)Running dogmon in the venv$(RESET)"
	@echo -e -n "$(DIM)"
	@ . $(VENV_DIR)/bin/activate ;\
	dogmon
	@echo -e -n "$(RESET)"

docker-build: $(STAMP_DIR)/.docker-build-stamp ## Build a Docker image with dogmon
$(STAMP_DIR)/.docker-build-stamp: $(STAMP_DIR)/.dist-stamp
	@echo -e "$(BOLD)Building a Docker image with dogmon$(RESET)"
	@echo -e -n "$(DIM)"
	@docker build --file=./Dockerfile --tag=dogmon ./
	@touch $@
	@echo -e -n "$(RESET)"
	
docker-run: docker-build ## Run dogmon Docker image
	@echo -e "$(BOLD)Running dogmon Docker image$(RESET)"
	@echo -e -n "$(DIM)"
	@docker run -it --rm --name=dogmon -e USERID=$(shell id -u) -v /tmp/access.log:/tmp/access.log dogmon:latest
	@echo -e -n "$(RESET)"
	
clean: ## Remove temporary files
	@echo -e "$(BOLD)Removing temporary files$(RESET)"
	@rm -rf build dist src/dogmon.egg-info .pytest_cache $(STAMP_DIR)/.*-stamp *.log
	@find . -depth -type d -name __pycache__ -exec rm -rf {} \;
	@find . -type f -name "*.pyc" -delete

# Absolutely awesome: http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "$(BOLD)%-30s$(RESET) %s\n", $$1, $$2}'

.PHONY: venv install install-dev lint test ci dist run docker-build docker-run clean help
.DEFAULT_GOAL := help
