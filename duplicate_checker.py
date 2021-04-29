import os
import sys
import csv
import pandas as pd

#print(os.listdir())

filename = input('filename? ')
delimiter = input('delimiter? ')
encoding_list = ['utf-8', 'cp1252']

for enc in encoding_list:    
    try:
        print(f"[*]Trying encoding={enc}...", end='\t')
        file = pd.read_csv(filename, sep=delimiter, encoding=enc, low_memory=False)
        print('[OK]')
        break
    except FileNotFoundError:
        print(f"[!]No such file found in the current directory. Did you mean {filename}.csv?\nExiting...")
        input('Press ENTER to exit:')
        sys.exit()
    except UnicodeDecodeError:
        print('[Failed]')
    except ValueError:
        print(f"[!]Error: Enter the correct delimiter")
        input('Press ENTER to exit:')
        sys.exit()

duplicate = file[file.duplicated()]
dups = file.duplicated().sum()
print(f"{file.duplicated().sum()} duplicate records found.")

if dups > 0:
    clean_df = file.drop_duplicates()
    print(f"Writing clean records to csv...")
    clean_df.to_csv(f"{filename.split('.')[0]}_NO_DUPLI.csv", index=False)
    input('[SUCCESS] Press ENTER to exit: ')
