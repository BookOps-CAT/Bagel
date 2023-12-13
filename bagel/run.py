import sys

from ingest import form_data_reader
from produce import game_record, save2marc, generate_controlNo, _date_today
from download import get_metadata


def run(start_sequence: str) -> None:
    # retrieve data and identify start of sequence
    get_metadata()
    n = int(start_sequence)

    # define output file
    date = _date_today()
    out_file = f"temp/BaGEL-{date}.mrc"

    # read rows of data frame, generate controlNos, create bibs, write to MARC
    for data in form_data_reader():
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
