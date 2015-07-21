import re, csv

header_end = re.compile("\s+START\s+END\s+")

## p. 1172 is missing a space between the final date and the description. Can't understand why the layout option does this; a space is clearly visible. I dunno. 
five_data_re = re.compile("\s*([\w\d]+)\s+(\d\d\/\d\d\/\d\d\d\d)\s+(.*?)\s+(\d\d\/\d\d\/\d\d\d\d)\s+(\d\d\/\d\d\/\d\d\d\d)\s*(.+?)\s+([\d\.\-\,]+)\s*\Z")
five_data_missing_date = re.compile("\s*([\w\d]+)\s+(\d\d\/\d\d\/\d\d\d\d)\s+(.*?)\s{10,}(.*?)\s+([\d\.\-\,]+)\s*\Z")
three_data_re = re.compile("\s+(\w[\w\,\s\.\-\']+?)\s{10,}(\w.*?)\s{4,}([\d\.\-\,]+)\s*")

top_matter_end_re = re.compile("\s+DOCUMENT\s+NO\.\s+DATE\s+PAYEE")
funding_year_re = re.compile("\s*Funding\s+Year\s+(\d+)")
blank_line_re = re.compile("\s+\Z")

page_number_re = re.compile("\s+\w\-\d+")
page_number_alt_re = re.compile("\s+\w\-\d\-\d+")

continuation_with_amount_re = re.compile("\s*(.+?)\s{10,}([\d\.\-\,]+)\s+\Z")


travel_re = re.compile("\s+TRAVEL\s+AND\s+TRANSPORTATION\s+OF\s+PERSONS\s+")
it_re = re.compile("\s+INTERDEPARTMENTAL\s+TRANSPORTATION\s+")
ocs_re = re.compile("\s+OTHER\s+CONTRACTUAL\s+SERVICES\s+")
acq_re = re.compile("\s+ACQUISITION\s+OF\s+ASSETS\s+")
prsnl_re = re.compile("\s+PERSONNEL\s+BENEFITS\s+")
netpayroll_re = re.compile("\s+NET\s+PAYROLL\s+EXPENSES\s+")
persnl_comp_re = re.compile("\s+PERSONNEL COMP. FULL-TIME PERMANENT\s+")
other_personal_comp = re.compile("\s+OTHER PERSONNEL COMPENSATION\s+")
remployed_annuitants_re = re.compile("\s+RE-EMPLOYED ANNUITANTS\s+")
former_employee_benefits_re = re.compile("\s+BENEFITS FOR NON SENATE/FORMER PERSONNEL\s+")

page_number_re = re.compile("\s+B\s*\-\s*\d+\s*")

def is_subtotal(line):
    if travel_re.match(line):
        return True
    if it_re.match(line):
        return True
    if ocs_re.match(line):
        return True
    if acq_re.match(line):
        return True
    if prsnl_re.match(line):
        return True
    if netpayroll_re.match(line):
        return True
    if persnl_comp_re.match(line):
        return True   
    if other_personal_comp.match(line):
        return True
    if remployed_annuitants_re.match(line):
        return True
    if former_employee_benefits_re.match(line):
        return True
    
    return False

def compute_break_position(top_matter):
    return None
    
    for whole_line in top_matter:
        if top_matter_end_re.match(whole_line):
            break

        if blank_line_re.match(line):
            continue
    return None

def process_top_matter(page_num, top_matter):
    
    #top_matter_top_left_column_delimiter = compute_break_position(top_matter)
    top_matter_top_left_column_delimiter = 48
    #return None
    
    expense_description = ''
    for whole_line in top_matter:
        if top_matter_end_re.match(whole_line):
            break
        line = whole_line[:top_matter_top_left_column_delimiter]
        if blank_line_re.match(line):
            continue
            
        result = funding_year_re.match(line)
        line_stripped = line.strip()
        if line_stripped:
            expense_description += ' ' + line_stripped + ' '
        
    expense_description = re.sub( '\s+', ' ', expense_description ).strip()
    return expense_description


# some carryover lines have amounts in them, and some don't -- that is, they are just extensions of the text field. See, e.g. p. 1672.
def test_carryover_line(line_offset, line):
    # are the first n characters of the line empty ? 
    line_start = line[:line_offset]
    if blank_line_re.match(line_start):
        line_end = line[line_offset:]
        if not blank_line_re.match(line_end):
        
            #print "***possible continuation: %s" % (line_end)
            return True
    return False
    
def process_data_lines(page_num, data_lines):
    
    missing_data = []
    
    
    return_data = []
    return_data_index = 0
    
    # these are lines that describe prior lines--typically the travel associated with a per diem or a transportation line. They aren't processed in this step, but instead just recorded in the one_part_continuation_register, and processed after that. 
    one_part_continuation_register = []
    
    last_line_data_index = None
    for data_line in data_lines:
        #print "handling %s %s" % (last_line_data_index, data_line)
        if blank_line_re.match(data_line):
            # don't reset last line data index--sometimes the page number appears in the middle of a page. 
            continue
        
        if page_number_re.match(data_line):
            # These are the page numbers
            continue
            
        if is_subtotal(data_line):
            last_line_data_index = None
            #assert False
            continue
            
        found_data = five_data_re.match(data_line)
        if found_data:
            #print found_data.groups()
            if found_data:
                return_data.append(['five data line', False, page_num] + list(found_data.groups()))
                return_data_index += 1
                #print "index of text description is: " + str(found_data.start(6))
                last_line_data_index = str(found_data.start(6))
                #print "Five data---last line data index: %s %s" % (last_line_data_index, found_data.groups())
                # we need this to figure out if the next line is a continuation or a sub-header type thing.
    
        
        
        else:
            #pass
            found_data2 = three_data_re.match(data_line)
            found_data_missing_date = five_data_missing_date.match(data_line)
            
            if found_data2:
                results = list(found_data2.groups())
                result_formatted = ['three data line', False, page_num, '', '', results[0], '', '', results[1], results[2]]
                return_data.append(result_formatted)
                return_data_index += 1
                last_line_data_index = None
            
            elif (found_data_missing_date):
                print "**found missing date line"
                results = list(found_data_missing_date.groups())
                result_formatted = ['missing date line', False, page_num, results[0], results[1], results[2], '', '', results[3], results[4]]
                return_data.append(result_formatted)
                return_data_index += 1
                last_line_data_index = None
            
            else:
                is_page_num = page_number_re.match(data_line)
                is_page_num_alt = page_number_alt_re.match(data_line)
                if is_page_num or is_page_num_alt:
                    continue
                
                
                if last_line_data_index:
                    #print "running carryover test with n=%s" % (last_line_data_index)
                    carryover_found = test_carryover_line(int(last_line_data_index), data_line)
                    
                    if carryover_found:
                        continuation_data = continuation_with_amount_re.match(data_line)
                    
                        if continuation_data:
                            #print "two part continuation found: '" + continuation_data.group(1) + "'-'" + continuation_data.group(2) + "'"
                            # it's a two part continuation--probably per diem/travel. So add same data as for the first line.
                            previous_result = return_data[return_data_index-1]
                            result_formatted = ['continuation_data', True, previous_result[2], previous_result[3], previous_result[4], previous_result[5], previous_result[6], previous_result[7], continuation_data.group(1), continuation_data.group(2)]
                            return_data.append(result_formatted)
                            return_data_index += 1
                            
                        else:
                            description =  data_line.strip()
                            #print "one part continuation found: '" + description +"'"
                            register_data = {'array_index':return_data_index, 'data':description}
                            one_part_continuation_register.append(register_data)
                            ## annoyingly, these descriptions themselves can span over multiple lines. 
                            ## e.g. p. 1557:
                            # WASHINGTON DC TO CHARLESTON, COLUMBIA, CHARLESTON, COLUMBIA, LEXINGTON, 
                            # CLINTON, SPARTANBURG, GREENVILLE, COLUMBIA, AIKEN, COLUMBIA, CHARLESTON AND RETURN
                            # RETURN
                            ## append it to previous rows. 
                            
                     
                else:
                    print "missing <" + data_line + ">"
                    missing_data.append({'data':data_line, 'offset':return_data_index,'page_num':page_num })
    
    #if one_part_continuation_register:
        #print "one_part_continuation_register: %s" % (one_part_continuation_register)
    return {'data':return_data, 'register':one_part_continuation_register, 'missing_data':missing_data}
        
def find_header_index(line_array):
    matches = 0
    header_index = None
    for index, line in enumerate(line_array):
        r = header_end.search(line)
        if r:
            #print "match: %s: %s" % (index, line)
            matches += 1
            header_index = index
    
    # break if we don't find exactly one occurrence of this per page.
    assert matches == 1
    return header_index
    
    




start_page = 17
end_page = 2073

#start_page = 1938
#end_page = 1938


page_file_unfilled = "pages/layout_%s.txt"
header_index_hash = {}

csvfile = open("senate_data.csv", 'wb')
datawriter = csv.writer(csvfile)
current_description = None
description = None

missing_data_file = open("missing_data.txt", 'w')

for page in range(start_page, end_page+1):
    # random blank page
    if page == 1884 or page == 2068:
        continue
    print "Processing page %s" % page
    filename = page_file_unfilled % (page)
    fh = open(filename, 'r')
    page_array = []
    for line in fh:
        page_array.append(line)
    header_index = find_header_index(page_array)
    
    # keep stats on where we find the index.
    try:
        header_index_hash[header_index] += 1
    except KeyError:
        header_index_hash[header_index] = 1
    
    # This is based on research... 
    if header_index > 6:
        top_matter = page_array[:header_index+1]
        description = process_top_matter(page, top_matter)
    
    current_description = description

    data_lines = page_array[header_index+1:]
    data_found = process_data_lines(page, data_lines)
    # get the data lines, and the run-on lines.
    data_lines = data_found['data']
    one_line_continuation_register = data_found['register']
    
    # run through the continuation lines and append them to the right places.
    for cl in one_line_continuation_register:
        all_related_lines_found = False
        current_line_position = cl['array_index']-1
        
        while all_related_lines_found == False:
            data_lines[current_line_position][8] = data_lines[current_line_position][8] + " + " + cl['data']
            if data_lines[current_line_position][0] != 'continuation_data':
                all_related_lines_found = True
            else:
                # it's a continuation line, so append this to the previous line too. 
                current_line_position -= 1
    
    for data in data_lines:
        datawriter.writerow([current_description] + data)

    if data_found['missing_data']:
        
        missing_data_file.write(str(data_found['missing_data']) + "\n")
    
for k,v in sorted(header_index_hash.items()):
    print k,v
    
"""
header index frequency:
3 1240
18 117
19 33
20 34
26 9
27 16
28 349
29 12
"""
    
