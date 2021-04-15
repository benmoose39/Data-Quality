from openpyxl import Workbook
import csv


wb = Workbook()
ws = wb.active
csv_file = input('Enter filename (eg: file.csv): ')
with open(csv_file, 'r') as f:
    for row in csv.reader(f):
        ws.append(row)
wb.save(f"converted_{csv_file.split('.')[0]}.xlsx")
print(f"[*]Created converted_{csv_file.split('.')[0]}.xlsx")
input('[SUCCESS]Press Enter to exit...')
