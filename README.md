# prometric-scheduler

# Automated Website Interaction with Selenium

## Overview

This project automates website interaction using Selenium WebDriver in Python. It includes scripts for installing Python, setting up dependencies, and scheduling a task to run a Python script periodically. Automation is done in python script.

## Contents

1. [Installer Script (`install_python_and_dependencies.bat`)](#installer-script-install_python_and_dependenciesbat)
2. [Scheduler Script (`schedule_script.bat`)](#scheduler-script-schedule_scriptbat)
3. [Python Script (`proscheduler.py`)](#python-scheduler-script-proschedulerpy)

## Installer Script (`install_python_and_dependencies.bat`)

This script automates the installation of Python, pip, required Python packages, and ChromeDriver.

### Usage

1. Run `install_python_and_dependencies.bat` as an administrator.
2. Follow the prompts to install Python and dependencies.

## Scheduler Script (`schedule_script.bat`)

This script sets up a scheduled task to run a Python script periodically.

### Usage

1. Ensure Python and dependencies are installed using the installer script.
2. Run `schedule_script.bat` to configure the scheduled task.
4. The Python script will be executed every hour.

## Python Script (`proscheduler.py`)

This script automates the website interaction and prints any available dates for a given test center.

### Usage

1. The Python script specified in the script will be executed based on the specified schedule.

### Important Notes

- specify month and year in month_year.txt file .i.e "12 2023"

## Support

For any issues or questions, feel free to [create an issue](https://github.com/your-username/your-repository/issues).

## License

This project is licensed under the [MIT License](LICENSE).
