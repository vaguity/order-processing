# Misen manual order processing script

## Setup

### Python virtual environment

- Create directory and set up virtual environment: `python3 -m venv .`
- Activate environment: `source bin/activate`
- Deactivate environment when done: `deactivate`

### Settings file

Copy `settings.example.json` to `settings.json`.

### Updating script with git

In the Terminal, while in this directory:

- `git fetch`
- `git pull`

## Guide

- Put files in `./import/[date].csv`
- Update the date in `settings.json` to correspond to the file in the import directory
- Run `python orders.py`
- Exported file will be created in `./export/[date]` directory
- If you want `-1` appended to order numbers, set `addons` parameter to `true` in `settings.json`
- If there are issues with the export, the terminal will flag error messages and log them to an error file in the export directory.
- The following errors are logged, and they do not prevent the export from being created:
    - For U.S. and Canada, state value is longer than two characters.
    - Postal code is longer than 11 characters.
    - Postal code contains characters other than alphanumeric characters or dashes.
    - Country code is not included in international shipping dictionary.


## Import settings

Set in `settings.json`.

### `date`

_String._ Corresponds to a filename in `./import/` and then creates a directory and file in `./export/`. Suggested formats are `20210601` and `20210601-1`, but any format works.

### `addons`

_Boolean._ When `true`, appends `-1` to all order numbers in the exported file.

## Script settings

Found in `orders.py`.

### `STATE_ABBREV`

_Dictionary._ Legacy for mapping common invalid state names for Fosdick import. Shouldn't be needed.

### `SKU_PRICING`

_Dictionary._ Maps SKUs to base prices and shipping rates. Each SKU corresponds to a list where the first value is the base price, and the second value is the base shipping rate.

### `INTL_SHIPPING`

_Dictionary._ Maps country codes to base shipping rates. This value replaces the shipping rate for each line item when calculating shipping.
