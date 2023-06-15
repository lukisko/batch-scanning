# how to run this app

- ```python -m pip install -r requirements.txt```
- ```gunicorn --bind 0.0.0.0:5000 app:app```
    - if you want to output it to a log file then specify ```gunicorn --bind 0.0.0.0:5000 --capture-output --error-logfile gunicorn.log app:app &```