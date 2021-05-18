# Misen manual order processing script

## Python virtual environment setup

- Create directory and set up virtual environment: `python3 -m venv .`
- Activate environment: `source bin/activate`
- Deactivate environment when done: `deactivate`

## Updating script with git

In the Terminal, while in this directory:

- `git add -A`
- `git reset --hard`
- `git fetch`
- `git pull`

You will need to update the date in `orders2.py` after running these commands, even if you've already updated the date.

## Guide

- Put files in `./import/[date].csv`
- Update the date in `settings.json` to correspond to the file in the import directory
- Run `python orders.py`
- Exported file will be created in `./export/[date]` directory
