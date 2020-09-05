import xlrd
import json
from os import path
import re
import csv

results = {}
keys = None

for i in range(17, 20):
    # load file
    filename = "./raw_/raw_fanta/{}.xlsx".format(i)
    xl_workbook = xlrd.open_workbook(filename)
    xl_sheet = xl_workbook.sheet_by_index(0)

    # foreach footballer get data
    for row_idx in range(2, xl_sheet.nrows):
        name = xl_sheet.cell(row_idx, 2).value.lower()
        if name not in results:
            results[name] = {}

        rigori = xl_sheet.cell(row_idx, 10).value
        results[name][i] = {
            "fanta": xl_sheet.cell(row_idx, 6).value,
            "goals": xl_sheet.cell(row_idx, 7).value + rigori,
            "assist": xl_sheet.cell(row_idx, 13).value,
            "played": xl_sheet.cell(row_idx, 4).value,
            "vote": xl_sheet.cell(row_idx, 5).value,
            "rigori": rigori,
        }
        if not keys:
            keys = list(results[name][i].keys())


# final results
final = {}
for foot in results:
    summary = []
    for stat in keys:
        rss = []
        for i in range(17, 20):
            if i in results[foot]:
                rss.append(str(results[foot][i][stat]))
            else:
                rss.append('**')
        summary.append("-".join(rss))
    final[foot] = " | ".join(summary)


with open('./results/stats.json', 'w') as fout:
    json.dump(final, fout)
