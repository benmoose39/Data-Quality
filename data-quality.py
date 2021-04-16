import pandas as pd
from openpyxl import Workbook
import csv
import math
import sys
import os

def excel_to_csv(file):
    df = pd.DataFrame(pd.read_excel(file))
    df.to_csv(f"{file.split('.')[0]}.csv", index=False)
    print(f'[*]Converted the file to {file.split(".")[0]}.csv')
    return file.split('.')[0] + '.csv'


def profile():
    all_csv = []
    for file in os.listdir():
        if '.csv' in file:
            all_csv.append(file)

    null_sheet = pd.read_csv(f"report_{filename.split('.')[0]}.csv")
    distinct_sheet = pd.read_csv(f"excel_output_{filename.split('.')[0]}.csv")

    wb = Workbook()

    writer = pd.ExcelWriter(f"Profile_{filename.split('.')[0]}.xlsx")

    null_sheet.to_excel(writer, 'NULL and UNIQUE', index=False)
    distinct_sheet.to_excel(writer, 'DISTINCT VALUES', index=False)

    writer.save()
    print('-' * 50)
    print(f"[SUCCESS]Profile_{filename.split('.')[0]}.xlsx created")
    print('-' * 50)
    

def clean():
    rem = input('[?]Remove temporary files?(y/N): ')
    if rem == 'y' or rem == 'Y':
        os.remove(f"excel_output_{filename.split('.')[0]}.csv")
        os.remove(f"report_{filename.split('.')[0]}.csv")
        os.remove(f"report_{filename.split('.')[0]}.txt")
        os.remove(f"..\\{filename}")
        print('[*]Removed temporary files')


def distinct_value_reporter(file):
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

    print(f"[*] Writing data to excel_output_{filename} ---")
    dict = {'Column' : attributes, 'Distinct Value' : uniq_val, 'Count' : val_count}
    df = pd.DataFrame(dict)
    df.to_csv(f"excel_output_{filename}", index=False)

    #input('[SUCCESS] Press ENTER to exit...')


def null_unique_reporter(file):
    rows = len(file)
    print(f"[INFO]\n[*]rows: {rows}\n[*]columns: {len(list(file.columns))}")

    print('*****************NULL*********************')
    null_count = list(file.isnull().sum())

    column_list = []
    null_list = []
    null_percent =[]

    for column in list(file.columns):
        null_in_col = file[column].isnull().sum()
        #print(f"{column} \t {null_in_col} \t {round(null_in_col*100/rows, 3)}")
        column_list.append(column)
        null_list.append(null_in_col)
        null_percent.append(round(null_in_col*100/rows, 3))

    null_df = pd.DataFrame({'Attribute':column_list, 'NULL_count':null_list, 'Percentage':null_percent}, index=['' for i in range(len(list(file.columns)))])
    print(null_df)
    print('\n')

    print('*****************UNIQUE*********************')
    distinct_list = []
    distinct_percent = []
    for column in list(file.columns):
        distinct = len(list(file[column].unique()))
        if file[column].isnull().any():
            distinct -= 1
        #print(f"{column} \t {distinct} \t {round(distinct*100/rows, 3)}")
        distinct_list.append(distinct)
        distinct_percent.append(round(distinct*100/rows, 3))
    distinct_df = pd.DataFrame({'Attribute':column_list, 'Distinct_count':distinct_list, 'Percentage':distinct_percent}, index=['' for i in range(len(list(file.columns)))])
    print(distinct_df)


    write = input('[?]Write to txt? (y/N)')
    if write == 'y' or write == 'Y':
        out_file = 'report_'+filename.split('.')[0]+'.txt'
        print(f'[*]Writing to {out_file} ---')
        
        with open(out_file, 'w') as f:
            f.write('********************NULL*********************\n')
            f.write(null_df.to_string())
            f.write('\n\n\n\n\n\n\n')
            f.write('******************DISTINCT*******************\n')
            f.write(distinct_df.to_string())

    write = input('[?]Write to csv? (y/N)')
    if write == 'y' or write == 'Y':
        df = pd.DataFrame({'Attribute':column_list, 'NULL_count':null_list, 'NULL_Percentage':null_percent, 'Distinct_count':distinct_list, 'Distinct_Percentage':distinct_percent})
        print(f'[*]Writing to report_{filename} ---')
        df.to_csv(f'report_{filename}', index=False)

    
#Start------------------------------------------------------------------------------------------------------------------------------------------------------------------
flag = False        
filename = input('[?]Name of file to read: ')
if '.' not in filename:
    print(f'[!]Did you mean {filename}.csv?')
    input('Press ENTER to exit:')
    sys.exit()

if filename.split('.')[-1] == 'xlsx':
    filename = excel_to_csv(filename)
    flag = True
    
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

try:
    os.chdir(f"Output_{filename.split('.')[0]}")
except FileNotFoundError:
    print(f"[*]Creating folder- output_{filename.split('.')[0]}")
    os.mkdir(f"Output_{filename.split('.')[0]}")
    os.chdir(f"Output_{filename.split('.')[0]}")
finally:
    null_unique_reporter(file)
    distinct_value_reporter(file)
    profile()
    clean()

    input('[SUCCESS]Press ENTER to exit...')

