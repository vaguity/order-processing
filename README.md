# Misen manual order processing script

## Python virtual environment setup

- Create directory and set up virtual environment: `python3 -m venv .`
- Activate environment: `source bin/activate`
- Deactivate environment when done: `deactivate`

## Settings file

Copy `settings.example.json` to `settings.json`.

## Updating script with git

In the Terminal, while in this directory:

- `git fetch`
- `git pull`

## Guide

- Put files in `./import/[date].csv`
- Update the date in `settings.json` to correspond to the file in the import directory
- Run `python orders.py`
- Exported file will be created in `./export/[date]` directory

