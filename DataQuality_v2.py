print(r'''
 _____________________________________________________________
|   ____        _            ___              _ _ _           |
|  |  _ \  __ _| |_ __ _    / _ \ _   _  __ _| (_) |_ _   _   |
|  | | | |/ _` | __/ _` |  | | | | | | |/ _` | | | __| | | |  |
|  | |_| | (_| | || (_| |  | |_| | |_| | (_| | | | |_| |_| |  |
|  |____/ \__,_|\__\__,_|___\__\_\\__,_|\__,_|_|_|\__|\__, |  |
|                      |_____|         Version: 2.0   |___/   |
|                                                             |
|  Author: BenMoose39           Initial Release: 12-Apr-2021  |
|  https://github.com/benmoose39/Data-Quality                 |
|_____________________________________________________________|
''')
###########################################################
def end():
    input(f"Press ENTER to exit...")
    sys.exit()
    
###########################################################
def import_dependencies():
    print(f"[*] Checking dependencies... ", end='')
    while(True):
        try:
            global pd
            import pandas as pd
            import csv
            from openpyxl import Workbook
            print(f"[OK]")
            break
        except ModuleNotFoundError as nomodule:
            print(f"\n[!] {nomodule}")
            module = str(nomodule)[17:-1]
            if input(f"[?] Attempt to install {module}?(y/N) ") in yes:
                if os.system(f"pip install {module}") == 0:
                    continue
            print(f"[!] Unable to install {module}. Try manually and come back")
            end()
    return

############################################################
def csv_to_excel(filename, df):
    print(f"[*] Converting to excel... ", end='')
    writer = pd.ExcelWriter(f"converted_{filename}.xlsx")
    df.to_excel(writer, index=False)
    writer.save()
    print(f"[OK]")

    return
    
############################################################
def excel_to_csv(filename):
    try:
        file = pd.DataFrame(pd.read_excel(f"{filename}.xlsx"))
        print(f'[*] Converting file to {filename}.csv... ', end='')
        file.to_csv(f"{filename}.csv", index=False)
        print(f"[OK]")
    except FileNotFoundError:
        print(f"[!] File not found in current directory")
        end()
    return

############################################################
def file_import(file):
    excel = False
    csv = False
    if file not in os.listdir():
        print(f"[!] File not found in current directory")
        end()
    if file.endswith('.xlsx'):
        excel = True
    elif file.endswith('.csv'):
        csv = True
    else:
        print(f"[!] Unsupported file format.")
        end()
    filename = '.'.join(file.split('.')[:-1])

    if excel:
        excel_to_csv(filename)
    
    return filename, excel, csv

############################################################
def dataframe(filename):
    delimiter = input('[?] Delimiter? ')
    encoding_list = ['utf-8', 'cp1252']

    for enc in encoding_list:    
        try:
            print(f"[*] Trying encoding={enc}...", end='\t')
            df = pd.read_csv(f"{filename}.csv", sep=delimiter, encoding=enc, low_memory=False)
            print('[OK]')
            return df
        except UnicodeDecodeError:
            print('[Failed]')
        except ValueError:
            print(f"\n[!] Error: Enter the correct delimiter")
            end()

############################################################
def choose():
    print("[*] Choose:")
    print("1) Convert to csv")
    print("2) Convert to excel(beta)")
    print("3) Check for duplicate records")
    print("4) Profile the dataset")
    print("5) Quit")
    while True:
        try:
            option = int(input('[?] Enter your option: '))
            if option == 5:
                end()
            elif option not in range(1,6):
                print('[!] Invalid option')
                continue
            break
        except ValueError:
            print("[!] Options are 1,2,3,4,5")
    return option

############################################################
def null_unique_report(file):
    rows = len(file)
    print(f"[INFO]\n[*] Rows: {rows}\n[*] Columns: {len(list(file.columns))}")
    print(f"[*] Number of duplicate records: {file.duplicated().sum()}")

    null_count = list(file.isnull().sum())

    column_list = []
    null_list = []
    null_percent =[]
    for column in list(file.columns):
        null_in_col = file[column].isnull().sum()
        column_list.append(column)
        null_list.append(null_in_col)
        null_percent.append(round(null_in_col*100/rows, 3))

    null_df = pd.DataFrame({'Attribute':column_list, 'NULL_count':null_list, 'Percentage':null_percent}, index=['' for i in range(len(list(file.columns)))])

    distinct_list = []
    distinct_percent = []
    for column in list(file.columns):
        distinct = len(list(file[column].unique()))
        if file[column].isnull().any():
            distinct -= 1
        distinct_list.append(distinct)
        distinct_percent.append(round(distinct*100/rows, 3))
    distinct_df = pd.DataFrame({'Attribute':column_list, 'Distinct_count':distinct_list, 'Percentage':distinct_percent}, index=['' for i in range(len(list(file.columns)))])

    df = pd.DataFrame({'Attribute':column_list, 'NULL_count':null_list, 'NULL_Percentage':null_percent, 'Unique_count':distinct_list, 'Unique_Percentage':distinct_percent})
    print(f'[*]Writing to report_{filename}.csv ...', end='')
    df.to_csv(f'report_{filename}.csv', index=False)
    print(f'[OK]')

    write = input('[?]Write to txt? (y/N)')
    if write == 'y' or write == 'Y':
        print(f'[*]Writing to report_{filename}.txt ...', end='')
            
        with open(f"report_{filename}.txt", 'w') as f:
            f.write(f"[INFO]\n[*]Rows: {rows}\n[*]Columns: {len(list(file.columns))}\n")
            f.write(f"[*]Number of duplicate records: {file.duplicated().sum()}\n\n")
            f.write('********************NULL*********************\n')
            f.write(null_df.to_string())
            f.write('\n\n\n')
            f.write('******************DISTINCT*******************\n')
            f.write(distinct_df.to_string())

        print(f'[OK]')
    return df

############################################################
def distinct_report(file):
    rem = len(list(file))
    file = file.replace(math.nan, 'NULL', regex = True)

    attributes = []
    uniq_val = []
    val_count = []

    flag = False
        
    print(f"\n[*] Finding distinct values---")
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
            
        rem -= 1
        print(f"[*] {rem} attributes remaining. Current attribute: {column}")
            
        attributes.append('')
        uniq_val.append('')
        val_count.append('')

    print(f"[*] Writing data to distinct_values_{filename}.csv... ", end='')
    dict = {'Column' : attributes, 'Distinct Value' : uniq_val, 'Count' : val_count}
    df = pd.DataFrame(dict)
    df.to_csv(f"distinct_values_{filename}.csv", index=False)
    print(f"[OK]")

    return df

############################################################
def profile(null_sheet, distinct_sheet):    
    print(f"[*] Writing to Profile_{filename}.xlsx...")
    wb = Workbook()
    writer = pd.ExcelWriter(f"Profile_{filename}.xlsx")

    try:
        null_sheet.to_excel(writer, 'NULL and UNIQUE', index=False)
        distinct_sheet.to_excel(writer, 'DISTINCT VALUES', index=False)
    except ValueError as v_error:
        print(f"[!] Error: {v_error}")
        print(f"[!] Suggestion: Split the distinct_value file and save as two separate files")
        end()

    writer.save()
        
    print('-' * 50)
    print(f"[SUCCESS]Profile_{filename}.xlsx created")
    print('-' * 50)
    return

############################################################
def check_duplicates(df):
    duplicate = df[df.duplicated()]
    dups = df.duplicated().sum()
    print(f"[*] {dups} duplicate records found.")
    if dups > 0:
        if input(f"[?] Create new csv with unique records?(y/N) ") in yes:
            clean_df = df.drop_duplicates()
            print(f"[*] Writing clean records to csv... ", end='')
            clean_df.to_csv(f"{filename}_NO_DUPLICATES.csv", index=False)
            print(f"[OK]")

############################################################
try:
    yes = ['y','Y']
    import sys
    import os
    import math
    import_dependencies()
    from openpyxl import Workbook
    
    file = input(f"[?] Name of file to read: ")
    filename, excel, csv = file_import(file)
    df = dataframe(filename)

    operation = choose()
    if operation == 1:
        if csv:
            print(f"[*] File is already in csv format")
        else:
            excel_to_csv(filename)
    elif operation == 2:
        if excel:
            print(f"[*] File is already in xlsx format")
        else:
            csv_to_excel(filename, df)
    elif operation == 3:
        check_duplicates(df)
    elif operation == 4:
        try:
            os.chdir(f"Output_{filename}")
        except FileNotFoundError:
            print(f"[*] Creating folder: Output_{filename}... ", end='')
            os.mkdir(f"Output_{filename}")
            print(f'[OK]')
            os.chdir(f"Output_{filename}")
            
        null_unique = null_unique_report(df)
        distinct = distinct_report(df)
        profile(null_unique, distinct)
        
    end()
except KeyboardInterrupt:
    print(f"[!] Stopped")
    end()


