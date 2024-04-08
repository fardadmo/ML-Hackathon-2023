MAGENTA=`tput setaf 5`
RESET=`tput sgr0`

all: acquire-data run-pipeline

setup-environment:
	@echo "Setup world"
	@conda env create -f environment.yaml
	@echo "${MAGENTA}Remember to activate your environment with these instructions ^${RESET}"

run-pipeline:
	@echo "Running pipeline"
	@python main.py --config_path=config.yaml --full_analysis False --partial False

format:
	@echo "Running autopep8 and isort to fix any formatting issues in the code"
	@autopep8 --in-place --recursive .
	@isort .

run-streamlit:
	streamlit run app.py -- --config_path=config.yaml