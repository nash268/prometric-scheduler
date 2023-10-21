@echo off

REM Specify Python executable and script paths
set PYTHON_EXECUTABLE="C:\Path\To\Your\Python\python.exe"
set PYTHON_SCRIPT="C:\Path\To\Your\Script\script.py"

REM Create a new task in Task Scheduler
schtasks /create /tn "MyPythonTask" /tr %PYTHON_EXECUTABLE% /sc hourly /mo 1

REM Set the start time to be now
schtasks /run /tn "MyPythonTask"

REM Open the Task Scheduler for further configuration
taskschd.msc