.DEFAULT_GOAL 	:= help

DEFAULT_CONFIG	= config.ini
CONFIG_ROOT 	= $(DEFAULT_CONFIG)
LABEL			= custom
CONFIG_FOLDER	= configurations/
NEW_CONFIG		= $(CONFIG_FOLDER)$(LABEL).ini

view: ## display the Makefile
	@cat Makefile

edit: ## open the Makefile with `code`
	@code Makefile

save: ## save the current `config.ini` file in configurations
	@cat $(DEFAULT_CONFIG) > $(NEW_CONFIG)

config: ## Run the app using the `config` mode and `config.ini` file
	@python main.py config

load: ## Run the app using the `config` mode and saved configuration file
	@python main.py config -p $(NEW_CONFIG)

help: ## Show this help
	@echo Makefile rules:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo
	@echo Run \"python main.py cmd -h\" for command line options