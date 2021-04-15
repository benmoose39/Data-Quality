import pandas as pd
import math
import sys

filename = input('Name of csv file to read(eg.: example.csv): ')
delimiter = input('Delimiter? ')

try:
    test = pd.read_csv(filename, sep=delimiter, low_memory=False)
except FileNotFoundError:
    print(f"[!] No such file found in the current directory. Did you mean {filename}.csv?\nExiting...")
    input('Press ENTER to exit:')
    sys.exit()
#test = test.replace(math.nan, 'NULL', regex = True)

#null_columns = test.columns[test.isnull().any()]
rows = len(test)
print(f"[INFO]\n[*]rows: {rows}\n[*]columns: {len(list(test.columns))}")

print('*****************NULL*********************')
null_count = list(test.isnull().sum())

column_list = []
null_list = []
null_percent =[]

for column in list(test.columns):
    null_in_col = test[column].isnull().sum()
    #print(f"{column} \t {null_in_col} \t {round(null_in_col*100/rows, 3)}")
    column_list.append(column)
    null_list.append(null_in_col)
    null_percent.append(round(null_in_col*100/rows, 3))

null_df = pd.DataFrame({'Attribute':column_list, 'NULL_count':null_list, 'Percentage':null_percent}, index=['' for i in range(len(list(test.columns)))])
print(null_df)
print('\n')

print('*****************UNIQUE*********************')
distinct_list = []
distinct_percent = []
for column in list(test.columns):
    distinct = len(list(test[column].unique()))
    if test[column].isnull().any():
        distinct -= 1
    #print(f"{column} \t {distinct} \t {round(distinct*100/rows, 3)}")
    distinct_list.append(distinct)
    distinct_percent.append(round(distinct*100/rows, 3))
distinct_df = pd.DataFrame({'Attribute':column_list, 'Distinct_count':distinct_list, 'Percentage':distinct_percent}, index=['' for i in range(len(list(test.columns)))])
print(distinct_df)


write = input('Write to txt? (y/N)')
if write == 'y' or write == 'Y':
    out_file = 'report_'+filename[:-4]+'.txt'
    print(f'[*]Writing to ./{out_file} ---')
    
    with open(out_file, 'w') as f:
        f.write('********************NULL*********************\n')
        f.write(null_df.to_string())
        f.write('\n\n\n\n\n\n\n')
        f.write('******************DISTINCT*******************\n')
        f.write(distinct_df.to_string())

write = input('Write to csv? (y/N)')
if write == 'y' or write == 'Y':
    df = pd.DataFrame({'Attribute':column_list, 'NULL_count':null_list, 'NULL_Percentage':null_percent, 'Distinct_count':distinct_list, 'Distinct_Percentage':distinct_percent})
    print(f'[*]Writing to ./report_{filename} ---')
    df.to_csv(f'report_{filename}', index=False)

input('[SUCCESS]Press ENTER to exit...')
