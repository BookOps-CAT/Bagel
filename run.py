import datetime
import os
import sys

from bagel.download import get_metadata
from bagel.ingest import form_data_reader
from bagel.produce import game_record, generate_controlNo, save2marc
from bagel.validate import validate_csv


def run(start_sequence: str) -> None:
    # retrieve data, validate csv and timestamps, identify start of sequence
    csvfile = get_metadata("temp/metadata.csv")
    valid_file = validate_csv(csvfile)
    if valid_file is False:
        exit()
    n = int(start_sequence)

    # define output file
    date = datetime.datetime.strftime(datetime.datetime.now(), "%y%m%d")
    suffix = 1
    out_file = f"temp/BaGEL-{date}-{suffix:02d}.mrc"
    while os.path.exists(out_file) and os.stat(out_file).st_size > 0:
        suffix += 1
        out_file = f"temp/BaGEL-{date}-{suffix:02d}.mrc"

    # read rows of data frame, generate controlNos, create bibs, write to MARC
    for data in form_data_reader(csvfile):
        if data.processing == "awaiting":
            controlNo = generate_controlNo(n)
            print(controlNo)
            rec = game_record(data, controlNo, suppressed=False, status_code="g")
            save2marc(rec, out_file)
            n += 1

    print("Completed...")
    print(f"Created {n - int(start_sequence)} bibs.")


if __name__ == "__main__":
    try:
        run(sys.argv[1])
    except IndexError:
        print("Invalid input. Provide next control # in sequence.")
