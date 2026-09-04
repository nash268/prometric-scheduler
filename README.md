# Prometric Scheduler

![Prometric Scheduler Screenshot](https://github.com/nash268/prometric-scheduler/assets/130772656/ddbcfd49-4a30-40bf-a6c2-42e85279884b)

**Prometric Scheduler** automates checking the Prometric website for available exam dates and alerts you as soon as seats open up.

📺 [Watch the tutorial video on YouTube](https://youtu.be/3JTJTnPMorY?si=uihAMKIiucfjl9nV)

> [!NOTE]
> By default, this checks **Pakistani centers only**. To check centers in a different country, see [Adding Centers for a Different Country](#adding-centers-for-a-different-country).

---

## Table of Contents

1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Running the Script](#running-the-script)
4. [Adding Centers for a Different Country](#adding-centers-for-a-different-country)
5. [Scheduling](#scheduling)
6. [Support](#support)
7. [License](#license)

---

## Requirements

- [Python](https://www.python.org/downloads/) installed
- [pip](https://pip.pypa.io/en/stable/installation/) installed

---

## Installation

1. **Download this repository** and extract the ZIP file.

   ![Download repository](https://github.com/nash268/prometric-scheduler/assets/130772656/44a47a1a-abfd-4a37-924a-1098ee968d6b)

2. **Open a terminal** in the `prometric-scheduler` folder — the same folder that contains `requirements.txt`.

3. **Install the required packages:**

   | OS | Command |
   |---|---|
   | Linux / macOS | `python3 -m pip install -r requirements.txt` |
   | Windows | `py -m pip install -r requirements.txt` |

---

## Running the Script

1. Open a terminal in the `prometric-scheduler` folder — the same folder that contains `proscheduler.py`.
2. Run the script:

   | OS | Command |
   |---|---|
   | Linux / macOS | `python3 proscheduler.py` |
   | Windows | `py proscheduler.py` |

   🎥 [See it running on Linux](https://github.com/nash268/prometric-scheduler/assets/130772656/68b5cdf8-58e7-4f98-80d4-ff1a2284c632)

3. **First run:** you'll be asked a few setup questions. Your answers are saved to `user_input.txt`.
4. **Later runs:** the script automatically reuses the saved values — no need to answer again.

> [!NOTE]
> **To update your saved values**, either:
> - Delete `user_input.txt` and rerun the script, **or**
> - Rerun the script with the `-e` flag:
>   ```
>   python3 proscheduler.py -e
>   ```

---

## Adding Centers for a Different Country

Run the script with the `-c` flag:

```
python3 proscheduler.py -c
```

This creates a `custom_centers.txt` file in the same folder, where your chosen centers are stored.

🎥 [Watch: adding custom centers](https://github.com/nash268/prometric-scheduler/assets/130772656/fca7c0f2-a02f-4d2b-bf44-9e6a4cd9934c)

> [!TIP]
> Don't rename any files in the `prometric-scheduler` folder — scheduling depends on the original file names.

---

## Scheduling

> [!CAUTION]
> Running this script will remove **all existing cron jobs** on Linux and macOS.

### Linux / macOS

- Scheduling is handled automatically via **crontab**.
- To customize the timing, use [crontab.guru](https://crontab.guru/#*/30_*_*_*_*) as a reference.
- Once you've found your seats 🎉 — remove the scheduled job by running:
  ```
  crontab -r
  ```

### Windows

- Scheduling is handled automatically via **Windows Task Scheduler**.
- After running the script, open **Task Scheduler** from the Start menu to confirm the task was created.
- Once you've found your dates, delete the task manually:

  ![Delete Windows scheduled task](https://github.com/nash268/prometric-scheduler/assets/130772656/ab513513-5a8f-4147-85ca-6f91b42f9fe5)

---

## Support

Having issues or questions? [Open an issue](https://github.com/nash268/prometric-scheduler/issues) on GitHub.

---

## License

Licensed under the [GNU General Public License v3.0](LICENSE).
