from xlrd import open_workbook
from xlutils.copy import copy
import json

COL_IDX = 7
FILE_NAMES = ["res", "res2", "stats"]    # same folder , .json
prices = {}
changes = [(1, COL_IDX, "prev."),
           (1, COL_IDX+1, "price"),
           (1, COL_IDX+2, "(2017-18-19) || fantavoto | goals | assist | p.giocate | voto_base | rigori")
           ]


def get_data(fnames):
    to_write = []
    for fn in fnames:
        with open('./{}.json'.format(fn), 'r') as fin:
            to_write.append(json.load(fin))
    return to_write


# load info (res->marks; res2->prices)
to_write = get_data(FILE_NAMES)

# read cells
rb = open_workbook("Quotazioni_Fantacalcio.xlsx")
xl_sheet = rb.sheet_by_index(0)
for row_idx in range(2, xl_sheet.nrows):
    name = xl_sheet.cell(row_idx, 2).value.lower()
    for i, dic in enumerate(to_write):
        if name in dic:
            changes.append((row_idx, COL_IDX+i, dic[name]))

wb = copy(rb)
w = wb.get_sheet(0)
for x, y, val in changes:
    w.write(x, y, val)


wb.save('fantaquote.xls')
