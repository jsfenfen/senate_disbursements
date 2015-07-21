# get all the office names in the spreadsheets.

import csv

file_list = ['112_sdoc4_senate_data.csv',
'112_sdoc7_senate_data.csv', '112_sdoc10_senate_data.csv', '113_sdoc2_senate_data.csv', '113_sdoc17_senate_data.csv']


office_dict = {}

for filename in file_list:
    reader = csv.reader(open(filename, 'r'))
    for line in reader:
        first_row = line[0]
        try:
            office_dict[first_row] = office_dict[first_row] + 1
        except KeyError:
            office_dict[first_row] = 1


writer = csv.writer(open("headerlist.csv", 'w'))
for key in office_dict.keys():
    print "%s - %s" % (key, office_dict[key])
    writer.writerow([key, office_dict[key]])
            