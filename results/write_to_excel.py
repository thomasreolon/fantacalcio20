from xlrd import open_workbook
from xlutils.copy import copy
import json

COL_IDX = 5
changes = [(1, 5, "Model Prevision")]
prices = {}

# millions
with open('./res2.json', 'r') as fin:
    prices = json.load(fin)


# marks
with open('./res.json', 'r') as fin:
    data = json.load(fin)


# read cells
rb = open_workbook("Quotazioni_Fantacalcio.xlsx")
xl_sheet = rb.sheet_by_index(0)
for row_idx in range(2, xl_sheet.nrows):
    name = xl_sheet.cell(row_idx, 2).value.lower()
    if name in data:
        changes.append((row_idx, COL_IDX, data[name]))
    if name in prices:
        changes.append((row_idx, COL_IDX+1, prices[name]))


wb = copy(rb)
w = wb.get_sheet(0)
for x, y, val in changes:
    w.write(x, y, val)


wb.save('fantaquote.xls')
