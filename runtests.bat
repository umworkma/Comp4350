@echo off
REM This batch file is in place to help simplify running the server locally
REM It will run the manage.py file using the python located in the venv folder
REM of your project source. This should be easily executed by simply double
REM clicking the batch file to run it.

venv\Scripts\python.exe manage.py runtests
pause
@echo on
