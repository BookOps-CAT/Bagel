# Bagel
 Scripts for ingesting data & producing MARC21 records for BPL Board Game Library

## Steps
0. Review submitted descriptions in data submission sheet
1. Mark records in the data submission sheet for processing (status "awaiting")
2. Download the sheet as csv
3. Ammend in run.py controlNo sequence (use the sheet for reference)
4. Run the script (run.py)
5. Validate produced records in MarcEdit (optional)
6. Load to Sierra using local (I) Load Overload New (insert or overlay) 
7. ~~Run suppression on the bibs~~
