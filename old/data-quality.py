print(r''' _____________________________________________________________
|   ____        _            ___              _ _ _           |
|  |  _ \  __ _| |_ __ _    / _ \ _   _  __ _| (_) |_ _   _   |
|  | | | |/ _` | __/ _` |  | | | | | | |/ _` | | | __| | | |  |
|  | |_| | (_| | || (_| |  | |_| | |_| | (_| | | | |_| |_| |  |
|  |____/ \__,_|\__\__,_|___\__\_\\__,_|\__,_|_|_|\__|\__, |  |
|                      |_____|                        |___/   |
|  Author: BenMoose39                  Released: 12-Apr-2021  |
|  https://github.com/benmoose39/Data-Quality                 |
|_____________________________________________________________|
''')


try:
    #Dependencies
    import sys
    import os

    print(f"[*]Checking for dependencies...", end='')
    try:
        import pandas as pd
        from openpyxl import Workbook
        import csv
        import math
        print("[OK]")
    except ModuleNotFoundError as nomodule:
        print(f"\n[!]{nomodule}")
        module = str(nomodule)[17:-1]
        print(f"[*]Run 'pip install {module}' and come back!!")
        input('Press ENTER to exit:')
        sys.exit()
        

    #converting the file in case it is .xlsx
    def excel_to_csv(file):
        df = pd.DataFrame(pd.read_excel(file))
        print(f'[*]Converting file to {file.split(".")[0]}.csv ...', end='')
        df.to_csv(f"{file.split('.')[0]}.csv", index=False)
        print(f'[OK]')
        return file.split('.')[0] + '.csv'


    #Profile and output data to .xlsx file
    def profile(null_sheet, distinct_sheet):
        #null_sheet = pd.read_csv(f"report_{filename.split('.')[0]}.csv")
        #distinct_sheet = pd.read_csv(f"distinct_values_{filename.split('.')[0]}.csv")

        print(f"[*] Writing to Profile_{filename.split('.')[0]}.xlsx...")
        wb = Workbook()

        writer = pd.ExcelWriter(f"Profile_{filename.split('.')[0]}.xlsx")

        try:
            null_sheet.to_excel(writer, 'NULL and UNIQUE', index=False)
            distinct_sheet.to_excel(writer, 'DISTINCT VALUES', index=False)
        except ValueError as v_error:
            print(f"[!] Error: {v_error}")
            print(f"[!] Suggestion: Split the distinct_value file and save as two separate files")
            input('Press ENTER to exit...')
            sys.exit()

        writer.save()
        
        print('-' * 50)
        print(f"[SUCCESS]Profile_{filename.split('.')[0]}.xlsx created")
        print('-' * 50)
        

    #Removes unnecessary files
    def clean():
        rem = input('[?]Remove temporary files?(y/N): ')
        if rem == 'y' or rem == 'Y':
            try:
                os.remove(f"distinct_values_{filename.split('.')[0]}.csv")
                os.remove(f"report_{filename.split('.')[0]}.csv")
                os.remove(f"report_{filename.split('.')[0]}.txt")
            except FileNotFoundError:
                pass
            finally:
                if excel:
                    os.remove(f"../{filename}")
                print('[*]Removed temporary files')


    #outputs all distinct values to .txt(optional) and .csv
    def distinct_value_reporter(file):
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
                #print(f"{attributes[-1]} \t {item} \t {val_count[-1]}")

            rem -= 1
            print(f"[*] {rem} attributes remaining. Current attribute: {column}")
            
            attributes.append('')
            uniq_val.append('')
            val_count.append('')

        print(f"[*] Writing data to distinct_values_{filename} ...", end='')
        dict = {'Column' : attributes, 'Distinct Value' : uniq_val, 'Count' : val_count}
        df = pd.DataFrame(dict)
        df.to_csv(f"distinct_values_{filename}", index=False)
        print(f"[OK]")

        return df

        #input('[SUCCESS] Press ENTER to exit...')


    def null_unique_reporter(file):
        rows = len(file)
        print(f"[INFO]\n[*]rows: {rows}\n[*]columns: {len(list(file.columns))}")
        print(f"[*]Number of duplicate records: {file.duplicated().sum()}")

        #print('*****************NULL*********************')
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
        #print(null_df)
        #print('\n')

        #print('*****************UNIQUE*********************')
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
        #print(distinct_df)


        df = pd.DataFrame({'Attribute':column_list, 'NULL_count':null_list, 'NULL_Percentage':null_percent, 'Unique_count':distinct_list, 'Unique_Percentage':distinct_percent})
        print(f'[*]Writing to report_{filename} ...', end='')
        df.to_csv(f'report_{filename}', index=False)
        print(f'[OK]')

        write = input('[?]Write to txt? (y/N)')
        if write == 'y' or write == 'Y':
            out_file = 'report_'+filename.split('.')[0]+'.txt'
            print(f'[*]Writing to {out_file} ...', end='')
            
            with open(out_file, 'w') as f:
                f.write(f"[INFO]\n[*]rows: {rows}\n[*]columns: {len(list(file.columns))}\n")
                f.write(f"[*]Number of duplicate records: {file.duplicated().sum()}\n\n")
                f.write('********************NULL*********************\n')
                f.write(null_df.to_string())
                f.write('\n\n\n\n')
                f.write('******************DISTINCT*******************\n')
                f.write(distinct_df.to_string())

            print(f'[OK]')
        return df

        
    #Start------------------------------------------------------------------------------------------------------------------------------------------------------------------
    excel = False        
    filename = input('[?]Name of file to read: ')
    if filename not in os.listdir():
        print(f'[!]No such file found. Did you mean {filename}.csv?')
        input('Press ENTER to exit:')
        sys.exit()

    elif filename.split('.')[-1] not in ['xlsx', 'csv']:
        print(f'[!]Unsupported file type')
        input('Press ENTER to exit:')
        sys.exit()

    if filename.split('.')[-1] == 'xlsx':
        try:
            filename = excel_to_csv(filename)
            excel = True
        except FileNotFoundError:
            print('[!]No such file found.')
            input('Press ENTER to exit:')
            sys.exit()
        
    delimiter = input('[?]Delimiter? ')
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

    try:
        os.chdir(f"Output_{filename.split('.')[0]}")
    except FileNotFoundError:
        print(f"[*]Creating folder- Output_{filename.split('.')[0]} ...", end='')
        os.mkdir(f"Output_{filename.split('.')[0]}")
        print(f'[OK]')
        os.chdir(f"Output_{filename.split('.')[0]}")
    finally:
        null_sheet = null_unique_reporter(file)
        distinct_sheet = distinct_value_reporter(file)
        profile(null_sheet, distinct_sheet)
        clean()

        input('[SUCCESS]Press ENTER to exit...')
except KeyboardInterrupt:
    input('\n\n[!]Stopped\nPress ENTER to exit...')
finally:
    sys.exit()

