# get all the office names in the spreadsheets.

import csv
from parse_office_names import parse_office

header_row = ['source_doc', 'senator_flag', 'senator_name', 'raw_office', 'funding_year', 'fiscal_year', 'congress_number', 'reference_page', 'document_number', 'date_posted', 'start_date', 'end_date', 'description', 'salary_flag', 'amount', 'payee']

#file_list = ['112_sdoc4_senate_data.csv', '112_sdoc7_senate_data.csv', '112_sdoc10_senate_data.csv', '113_sdoc2_senate_data.csv', '113_sdoc17_senate_data.csv', '113_sdoc22_senate_data.csv']

file_list = ['114_sdoc4_senate_data.csv']


pre_header =  "This data was parsed on an experimental basis by the Sunlight Foundation from Senate disbursement reports. Please cite 'The Sunlight Foundation' in any usage.  For more information see the readme at http://assets-reporting.s3.amazonaws.com/1.0/senate_disbursements/readme.txt.\n"


#file_list = ['113_sdoc22_senate_data.csv',]

office_dict = {}

for filename in file_list:
    reader = csv.reader(open(filename, 'r'))
    cleaned_filename = filename.replace(".csv", "_cleaned.csv")
    source_doc = filename.replace("_senate_data.csv", "")
    fh = open(cleaned_filename, 'w')
    fh.write(pre_header)
    writer = csv.writer(fh)
    writer.writerow(header_row)
    
    for line in reader:
        office_raw = line[0]
        line_type = line[1]
        continuation_line = line[2]
        reference_page = line[3]
        transaction_id = line[4]
        date_posted = line[5]
        payee = line[6]
        start_date = line[7]
        end_date = line[8]
        description = line[9]
        amount = line[10]
        
        [senator_name, funding_year, fiscal_year, congress, office] = parse_office(office_raw)
        salary_flag = 0
        if line_type == 'three data line':
            salary_flag = 1
            
        senator_flag = 0 
        if senator_name:
            senator_flag = 1
        
        return_row = [source_doc, senator_flag, senator_name, office, funding_year, fiscal_year, congress, reference_page, transaction_id, date_posted, start_date, end_date, description, salary_flag, amount, payee]
        writer.writerow(return_row)


