# Bagel
 Scripts for ingesting data & producing MARC21 records for BPL Board Game Library

## Submission data

 Submission data is collected in [this spreadsheet](https://docs.google.com/spreadsheets/d/1Z8kWlHZXbnzP7OQWK3nLy7DEdxedPv2pW2pYodh6_dY/edit#gid=1152172600).

## Setup
 This project requires Python 3.12.
 1. Clone repository
 2. Navigate to project directory in terminal (examples assume commands are run in bash)
    * `cd Bagel`
 3. Create virtual environment
    * `python -m venv .venv` 
 4. Activate new virtual environment
    * `source ./.venv/scripts/activate`
 5. Install dependencies
    * `pip install -r requirements.txt`

## Steps
0. Review submitted descriptions in data submission sheet
1. Mark new rows in the data submission sheet for processing (status "awaiting")
2. Note the last control # in the sheet
3. Navigate to the project directory in terminal
    * `cd github/Bagel`
4. Activate project's virtual environment
    * `source ./.venv/scripts/activate`
5. Run the following Python command in terminal (the next control # in the example is 20)
    * `python run.py 20`
6. Review and validate produced records in MarcEdit (optional)
7. Load to Sierra using local (I) Load Overload New (insert or overlay) 
8. Mark processed rows as "completed"
9. Add loaded dates, new control #s and Sierra bib IDs to sheet