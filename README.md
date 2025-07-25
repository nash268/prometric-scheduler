# prometric-scheduler
![Screenshot 2024-04-04 12 35 44 PM](https://github.com/nash268/prometric-scheduler/assets/130772656/ddbcfd49-4a30-40bf-a6c2-42e85279884b)


## [Watch Tutorial Video on Youtube](https://youtu.be/3JTJTnPMorY?si=uihAMKIiucfjl9nV)

## Overview

This project automates website interaction on Prometric website, checks for available dates and alerts the user once seats are found.
> [!NOTE]
> It checks for Pakistani centers by default. To add other centers
> see section "[Adding centers for different country](#adding-centers-for-different-country)"

## Download and Install python and required packages
- download and install python https://www.python.org/downloads/
- make sure pip is installed https://pip.pypa.io/en/stable/installation/
- open cmd/terminal inside `prometric-scheduler` folder where `requirements.txt` file is located and run:
- on Linux/MacOs:
  ```
  python3 -m pip install -r requirements.txt
  ```
- on windows:
  ```
  py -m pip install -r requirements.txt
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
> OR run script with "-e" argument
> ```
> python3 proscheduler.py -e
> ```

### Adding centers for different country
- run script with "-c" argument to add other centers
```
python3 proscheduler.py -c
```
- this will create a `custom_centers.txt` file in same directory, and store centers

[Screen recording 2024-04-06 6.25.01 PM.webm](https://github.com/nash268/prometric-scheduler/assets/130772656/fca7c0f2-a02f-4d2b-bf44-9e6a4cd9934c)


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
