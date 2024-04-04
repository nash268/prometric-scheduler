# prometric-scheduler
![image](https://github.com/nash268/prometric-scheduler/assets/130772656/946ef3d1-c194-4d61-9472-5b7ddb338591)



## Overview

This project automates website interaction on Prometric website, checks for available dates and alerts the user once seats are found.
> [!NOTE]
> Currently it only checks Pakistani test centers

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
  
- [running script on linux](https://github.com/nash268/prometric-scheduler/assets/130772656/68b5cdf8-58e7-4f98-80d4-ff1a2284c632)






- When running the script for the first time, it will prompt you with a few relevant questions.
- The provided values are then saved in the `user_input.txt` file.
- Subsequent runs of the script will automatically load values from the `user_input.txt` file.
> [!NOTE]
> To update the stored values, simply delete the `user_input.txt` file and rerun the script.

> [!TIP]
> Do Not! change any file names in prometric-scheduler folder for scheduling to work properly.

> [!CAUTION]
> Script will remove all previous cronjobs on Linux & MacOs.

### Linux and MacOs
- For Linux and MacOS users, the script utilizes crontab for scheduling automatic runs. Visit [crontab.guru](https://crontab.guru/#*/30_*_*_*_*) to configure the timing.
- once you have found your seats(hooray!!🎉🥳), to remove all cronjobs run `crontab -r` command in terminal.
### Windows
- on Windows, script utilizes Windows Task Scheduler. after running the script, search task scheduler in start menu and see if the task is created.
- Delete Task once you have found your dates.
  ![image](https://github.com/nash268/prometric-scheduler/assets/130772656/ab513513-5a8f-4147-85ca-6f91b42f9fe5)




## Support

For any issues or questions, feel free to [create an issue](https://github.com/nash268/prometric-scheduler/issues).

## License

This project is licensed under the [MIT License](LICENSE).
