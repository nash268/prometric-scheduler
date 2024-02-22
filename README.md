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
- Download repository
  ![screenshot](https://github.com/nash268/prometric-scheduler/assets/130772656/8d228d2b-f1c0-40fe-91cf-6a777ffb80c9)
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
  
- [running script.webm](https://github.com/nash268/prometric-scheduler/assets/130772656/25eea251-1395-48bb-b81d-21e6ffa3bc6b)


- When running the script for the first time, it will prompt you with a few relevant questions.
- The provided values are then saved in the `user_input.txt` file.
- Subsequent runs of the script will automatically load values from the `user_input.txt` file.
- To update the stored values, simply delete the `user_input.txt` file and rerun the script.

> [!IMPORTANT]
> Do Not! change any file names in prometric-scheduler folder for scheduling to work properly.

### Linux and MacOs
- For Linux and MacOS users, the script utilizes crontab for scheduling automatic runs. Visit [crontab.guru](https://crontab.guru/#*/30_*_*_*_*) to configure the timing.
- once you have found your seats(hooray!!🎉🥳), to remove all cronjobs run `crontab -r` command in terminal.
### Windows
- on Windows, script utilizes Windows Task Scheduler. after running the script search task scheduler in start menu and see if the task is created.



## Support

For any issues or questions, feel free to [create an issue](https://github.com/nash268/prometric-scheduler/issues).

## License

This project is licensed under the [MIT License](LICENSE).
