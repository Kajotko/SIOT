@echo off
start "Weather" python "weather_collect.py"
start "Twitter" python "stream_starter.py"
exit