from ingest import form_data_reader
from produce import game_record, save2marc, generate_controlNo


if __name__ == "__main__":
    csv_file = (
        "./temp/B(a)GEL metadata submission form (Responses) - Form Responses 1.csv"
    )
    out_file = "./temp/BaGEL-220912.mrc"
    reader = form_data_reader(csv_file)
    n = 341
    for data in reader:
        if data.processing == "awaiting":
            n += 1
            controlNo = generate_controlNo(n)
            print(controlNo)
            rec = game_record(data, controlNo, suppressed=False, status_code="g")
            save2marc(rec, out_file)
