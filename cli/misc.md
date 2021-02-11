# Misc Useful Commads

## Create a checklist for flake8 errors

flake8 file.py | awk '{print "[ ] " $0}' >> {file}\_flake8.md

## Run sql command in sqlite3

sqlite3 mydatabase.db < sql_script.sql

## Checksum files

`shasum -a 256 /path/to/file /path/to/file2`

## Compress multiple files with spaces in the names

`find /path/to/files\ with\ spaces/**/* -exec echo -n '"{}" ' \; | xargs gzip`

## Misc TODO

- [ ] [Using history](https://www.howtogeek.com/465243/how-to-use-the-history-command-on-linux/)
- [ ] [Flake8 errors](https://gitlab.com/pycqa/flake8/-/issues/31)
- [ ] [base64 decoding/encoding](https://www.igorkromin.net/index.php/2017/04/26/base64-encode-or-decode-on-the-command-line-without-installing-extra-tools-on-linux-windows-or-macos/)
- [ ] [Linux/SysAdmin cheat sheet](https://cheatography.com/beersj02/cheat-sheets/linux-bash-and-system-administration/)
- [ ] [Bash prompt tips](https://opensource.com/article/17/7/bash-prompt-tips-and-tricks)
