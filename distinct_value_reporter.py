import pandas as pd
import math
import sys

filename = input('[?]Name of csv file to read(eg.: example.csv): ')
delimiter = input('[?]Delimiter? ')
enc = 'utf-8'
enc_opt = input('[?]Select encoding format:\n\t1 : utf-8\n\t2 : cp1252\nDEFAULT is utf-8\nEnter your option: ')
if enc_opt == '2':
    enc = 'cp1252'
    
try:
    file = pd.read_csv(filename, sep=delimiter, encoding=enc, low_memory=False)
except FileNotFoundError:
    print(f"[!] No such file found in the current directory. Did you mean {filename}.csv?\nExiting...")
    input('Press ENTER to exit:')
    sys.exit()
except UnicodeDecodeError:
    print(f"[!] Error: Try changing encoding format")
    input('Press ENTER to exit:')
    sys.exit()

rem = len(list(file))

file = file.replace(math.nan, 'NULL', regex = True)

attributes = []
uniq_val = []
val_count = []

flag = False

print(f"[*] Total number of attributes: {rem}")
for column in list(file):
    flag = True
    values = list(file[column])
    values = ['NULL' if (value is None or value == '') else value for value in values]
    unique_list = list(file[column].unique())

    for item in unique_list:
        if item == '' or item is None:
            item = 'NULL'
        if flag:
            attributes.append(column)
            flag = False
        else:
            attributes.append('')
        uniq_val.append(item)
        val_count.append(values.count(item))
        #print(f"{attributes[-1]} \t {item} \t {val_count[-1]}")

    rem -= 1
    print(f"[*] {rem} attributes remaining. Current attribute: {column}")
    
    attributes.append('')
    uniq_val.append('')
    val_count.append('')

print(f"[*] Writing data to ./excel_output_{filename} ---")
dict = {'Column' : attributes, 'Distinct Value' : uniq_val, 'Count' : val_count}
df = pd.DataFrame(dict)
df.to_csv(f"excel_output_{filename}", index=False)

input('[SUCCESS] Press ENTER to exit...')
