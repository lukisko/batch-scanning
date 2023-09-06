# how to run this app

- ```python -m pip install -r requirements.txt```
- ```gunicorn --bind 0.0.0.0:5000 app:app```
    - if you want to output it to a log file then specify ```gunicorn --bind 0.0.0.0:5000 --capture-output --error-logfile gunicorn.log app:app &```

# additional requirements
- handle error from scanner
- handle empty files
- make correct order of pages (in case of pages over 10) - fixed in the newest version
- able to remove the last page