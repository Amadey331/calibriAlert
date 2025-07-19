@echo off

call %~dp0virtual\Scripts\activate


set TOKEN=6585331872:AAHCf10OaZKn6O79Lm9d2zsLM0nrPoB6Ljo
cd %~dp0
python calibriAlert.py

pause
