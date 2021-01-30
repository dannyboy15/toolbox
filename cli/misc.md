# Misc Useful Commads

## Create a checklist for flake8 errors
flake8 file.py | awk '{print "[ ] " $0}' >> {file}_flake8.md

## Run sql command in sqlite3
sqlite3 mydatabase.db < sql_script.sql
