COLOR_RESET=\033[0m
COLOR_YELLOW=\033[0;33m
COLOR_BLUE=\033[0;34m


DEBIAN_DEPENDENCIES = ruby ri ruby-bundler ruby-dev python3-pip make \
	build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev \
	wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev


ARCH_DEPENDENCIES = ruby ruby-bundler ruby-sqlite3 sqlite python python-pip wget curl ncurses

ECHO=echo -e

GEMFILE=Gemfile

VENV = venv
PIP = $(VENV)/bin/pip
PYTHON = $(VENV)/bin/python3

.PHONY: help, clean, setup, start, stop, clean, test



help: ## Show this help.
	@${ECHO} "${COLOR_YELLOW} ============= Welcome to Rontext ============= ${COLOR_RESET}"
	@${ECHO} " "
	@${ECHO} "Please use \`make ${COLOR_BLUE}<target>${COLOR_RESET}' where ${COLOR_BLUE}<target>${COLOR_RESET} is one of"
	@${ECHO} " "
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' ${MAKEFILE_LIST} | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "- ${COLOR_BLUE}%-30s${COLOR_RESET} %s\n", $$1, $$2}'


$(VENV)/bin/activate: requirements.txt
	@${ECHO} "${COLOR_YELLOW} Creating python virtual environment...... ${COLOR_RESET}"
	@python3 -m venv $(VENV)


debian-based-setup:
	sudo apt install -y $(DEBIAN_DEPENDENCIES)


arch-based-setup:
	sudo pacman -S $(ARCH_DEPENDENCIES)


start: setup ## Starts the application
	@${ECHO} "${COLOR_YELLOW} ============= Starting Rontext ============= ${COLOR_RESET}"
	@${ECHO} " "
	@${ECHO} "${COLOR_YELLOW} Running Rontext...... ${COLOR_RESET}"


setup: $(VENV)/bin/activate $(GEMFILE) ## Install the project dependencies
	@${ECHO} "${COLOR_YELLOW} Installing dependencies...... Python ${COLOR_RESET}"
	$(VENV)/bin/pip install -r requirements.txt
	@${ECHO} "${COLOR_YELLOW} Installing dependencies...... Ruby ${COLOR_RESET}"
	@sudo bundle install


clean: ## Clean up the project virtual environment and cache
	@${ECHO} "${COLOR_YELLOW} Cleaning up Rontext..... python cache ${COLOR_RESET}"
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -delete
	@${ECHO} "${COLOR_YELLOW} Cleaning up Rontext..... python virtual environment ${COLOR_RESET}"
	@rm -rf $(VENV) 
