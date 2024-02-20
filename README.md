# prometric-scheduler

# Automated Website Interaction with Selenium

## Overview

This project automates website interaction using Selenium WebDriver in Python and check for availability.

## Download and Install python and required packages
- download and install python https://www.python.org/downloads/
- install pip https://pip.pypa.io/en/stable/installation/
- open cmd or terminal and run:
  ```
  pip3 install selenium webdriver-manager
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


- on Linux/MacOS:
  ```
  python3 proscheduler.py
  ```
- on Windows:
  ```
  py proscheduler.py
  ```
  
[running script](https://github.com/nash268/prometric-scheduler/assets/130772656/527a7507-f5b7-4116-a172-07ed747a9572)

- running script for first time will ask you few relevant questions
- values are then stored in `user_input.txt`
- next time the script runs, values are loaded from `user_input.txt`
- to change values, delete `user_input.txt` and run script again




## Schedule the script to run on specific times:
### on MacOs and Linux you can use crontab:
- edit crontab file using following command: 
  ```
  crontab -e
  ```
- use [crontab.guru](https://crontab.guru/#*/30_*_*_*_*) to set timer.
- e.g ```*/30 * * * * cd ~/Downloads/prometric-scheduler/ && python3 proscheduler.py``` will run the script every 30 minutes 24/7.
- copypaste the line and save the crontab file
- once you have found your seats(hooray!!🎉🥳), to remove all cronjobs run ```crontab -r```command in terminal.

### On windows use task-scheduler:
- [watch youtube video](https://www.youtube.com/watch?v=IsuAltPOiEw&t=112s)

## Support

For any issues or questions, feel free to [create an issue](https://github.com/nash268/prometric-scheduler/issues).

## License

This project is licensed under the [MIT License](LICENSE).
