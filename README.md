# prometric-scheduler

# Automated Website Interaction with Selenium

## Overview

This project automates website interaction using Selenium WebDriver in Python and check for availability.

## Download and Install python and required packages
- download and install python https://www.python.org/downloads/
- install pip https://pip.pypa.io/en/stable/installation/
- open cmd or terminal and run:
  ```
  pip install selenium webdriver-manager
  ```
- if that doesn't work on windows. try:
  ```
  py -m pip install selenium webdriver-manager
  ```

## Python Script (`proscheduler.py`)
- [download repository](https://github.com/nash268/prometric-scheduler/archive/refs/heads/main.zip)
- extract zip file
- open terminal in the ``prometric-scheduler/`` folder where ``proscheduler.py`` is located
- inside cmd/terminal run:

on Windows:
  ```
  py proscheduler.py
  ```

on Linux/MacOS:
  ```
  python3 proscheduler.py
  ```
***

### Important Notes
- open ``proscheduler.py`` in any text editor(notepad)
- edit highlighted code to fit your needs
- ![image](https://github.com/nash268/prometric-scheduler/assets/130772656/ddd261ca-c924-47ea-a1f8-34095fbc2101)



- save changes and [run script](#python-script-proschedulerpy)


## Schedule the script to run on specific times:
### on MacOs and Linux you can use crontab:
  ```
  crontab -e
  ```
- use [crontab.guru](https://crontab.guru/#*/15_0-23_*_*_*) to set timer.
- e.g ```*/15 0-23 * * * cd ~/Downloads/prometric-scheduler/ && python3 proscheduler.py``` will run the script every 15 minutes 24/7.
- save the crontab file

### On windows use task-scheduler:
- [youtube.vid](https://www.youtube.com/watch?v=IsuAltPOiEw&t=112s)

## Support

For any issues or questions, feel free to [create an issue](https://github.com/nash268/prometric-scheduler/issues).

## License

This project is licensed under the [MIT License](LICENSE).
