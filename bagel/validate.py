# temp testing for google sheet validation

"""
add validation functions to the ingest module (or create a validate module?)
add after get_metadata() method in run.py
read data first?
validate the csv headings
validate the timestamp

list of column headings are in test_ingest.py

"""
import csv
import pandas as pd
from download import URL
from datetime import datetime


def validate_csv_headings():
    #
    # df = pd.read_csv(URL, usecols=range(0, 25))
    with open("temp/metadata.csv", "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        print(header)


def get_URL_headings():
    df = pd.read_csv(URL, usecols=range(0, 25))
    headers = df.columns.to_list()
    print(headers)


def validate_timestamp():
    # try to convert str in first column of csv to a timestamp based on format mapping
    with open("temp/metadata.csv", "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for n, row in enumerate(reader):
            try:
                timestamp = datetime.strptime(row[0], "%m/%d/%Y %H:%M:%S")
            except Exception:
                print(f"Invalid timestamp in row {n + 1}")
                raise
        print("All timestamps are valid.")
