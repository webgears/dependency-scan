# Dependency Scan

This project runs `yarn audit`, `yarn outdated`, `composer outdated` and `php security-checker.phar` and uploads the KPIs to a Google Spreadsheet.

## KPIs

Using yarn and composer this tool checks for the following KPIs:

- Outdated Patches: Number of dependencies where patch version differs from the latest version
- Outdated Minor: Number of dependencies where minor version differs from the latest version
- Outdated Major: Number of dependencies where major version differs from the latest version
- Security Issues Info: Number of security issues with a info level
- Security Issues Low: Number of security issues with a low level
- Security Issues Moderate: Number of security issues with a moderate level
- Security Issues High: Number of security issues with a high level
- Security Issues Critical: Number of security issues with a critical level

## Project Setup

Make sure you have [Pipenv](https://pipenv.readthedocs.io/en/latest/) installed.

Then run `pipenv install`. To execute the `main.py` script you can either run `pipenv run python main.py` or run `python shell` to load the pipenv environment into your shell.

## Usage

Skip 1-4 if you don't want to write the KPIs to a spreadsheet.

1. Create a new Spreadsheet and add the following columns
   > Date, Outdated Patches, Outdated Minor, Outdated Major, Security Issues Info, Security Issues Low, Security Issues Moderate, Security Issues High, Security Issues Critical
2. Enable Google Sheets API and get your credentials: https://console.developers.google.com/apis/credentials
3. Fetch the executeable from the releases
4. Download `credentials.json` and put it in the folder of the executeable
5. Ensure the binaries are installed and in the projects folder
6. Run the script with the arguments below 

For the first run uploading to a spreadsheet Google might ask you to open a browser and allow the requests.

```
./dependency-scan -i <SPREADSHEET_ID> -s <SHEET_NAME> -p <path> -y -c
```

### Arguments

```
-i|--spreadsheet_id <ID>    Google Spreadhsheet ID (Optional, omit if you don't want to send it to Google Spreedsheet)
-s|--sheet <NAME>           Sheet Name to add the data to (Optional, omit if you don't want to send it to Google Spreedsheet)
-p|--project <Path>         Project Folder to check (Optional)
-y|--yarn-audit             Run yarn audit (Optional)
-c|--composer-audit         Run composer audit (Optional)
--yarn-bin                  Path to yarn binary (Optional, defaults to "yarn")
--composer-bin              Path to composer binary (Optional, defaults to "composer")
--security-checker-bin      Path to sensiolabs security checker binary (Optional, defaults to "php security-checker.phar")
```

## Build

Run `pyinstaller --onefile -n dependency-scan main.py`. This will build the executeable for your machine.
For more info please read the info on [PyInstaller](https://www.pyinstaller.org/).

