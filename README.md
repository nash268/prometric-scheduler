# prometric-scheduler


## Overview

This project automates website interaction on Prometric website, checks for available dates and alerts the user once seats are found.

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
  ![image](https://github.com/nash268/prometric-scheduler/assets/130772656/44a47a1a-abfd-4a37-924a-1098ee968d6b)
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
  
- [running script on linux.webm](https://github.com/nash268/prometric-scheduler/assets/130772656/1ea57bf2-bd16-477c-91b0-93b5549af06f)



- When running the script for the first time, it will prompt you with a few relevant questions.
- The provided values are then saved in the `user_input.txt` file.
- Subsequent runs of the script will automatically load values from the `user_input.txt` file.
> [!NOTE]
> To update the stored values, simply delete the `user_input.txt` file and rerun the script.

> [!IMPORTANT]
> Do Not! change any file names in prometric-scheduler folder for scheduling to work properly.

> [!CAUTION]
> Script will remove all previous cronjobs on Linux & MacOs.

### Linux and MacOs
- For Linux and MacOS users, the script utilizes crontab for scheduling automatic runs. Visit [crontab.guru](https://crontab.guru/#*/30_*_*_*_*) to configure the timing.
- once you have found your seats(hooray!!🎉🥳), to remove all cronjobs run `crontab -r` command in terminal.
### Windows
- on Windows, script utilizes Windows Task Scheduler. after running the script, search task scheduler in start menu and see if the task is created.
- Delete Task once you have found your dates.
  
![image](https://github.com/nash268/prometric-scheduler/assets/130772656/6a5ae47a-7c78-416a-a212-555d061ff3e8)



## Support

For any issues or questions, feel free to [create an issue](https://github.com/nash268/prometric-scheduler/issues).

## License

This project is licensed under the [MIT License](LICENSE).
