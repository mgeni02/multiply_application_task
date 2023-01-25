# Specific instructions
# 0. This code is written and tested in Python >= 3.6
# 1. Do not use any libraries that are not part of the python stndard lib
# 2. What is given here is a guide, while it is meant to be useful, 
# you are free to modify any part of it as you wish

import csv

from ingest import MerchantDataFileHandler

output_file = 'db_ready_output.csv'

if __name__ == '__main__':
    try:
        mdfh = MerchantDataFileHandler(27)
        out_rows, out_err = mdfh.generate_output_file_contents()
        if out_rows:
            with open(output_file, 'w') as dbfile:
                fieldnames = out_rows[0].keys()
                writer = csv.DictWriter(dbfile, fieldnames = fieldnames)
                writer.writeheader()
                writer.writerows(out_rows)
    except ValueError as e:
       print(e)
    

