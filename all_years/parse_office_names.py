import re


senate_office_re = re.compile("SENATOR\s+([\w\.\s\,\(\)]+)\s+Funding Year (\d+)\s")
funding_year_re = re.compile(".+Funding Year ([\dX]+)\s.*", re.I)
congress_no = re.compile(".+\((11\d)TH\)\s.*")
fy_re = re.compile(".+ FY (201\d) .*")

def parse_office(office):
    funding_year = ""
    fiscal_year = ""
    congress = ""
    senator_name = ""
    # sometimes this gets in
    office = office.replace("DOCUMENT NO. DATE POSTED", "")
    
    if office.startswith("SENATOR"):
        
        found_data = senate_office_re.match(office)
        if found_data:
            results = list(found_data.groups())
            funding_year = results[1]
            senator_name = results[0]
            #print "Found %s - %s" % (results[0], results[1])
            
        else:
            print "No senate match in *** " +  office
        
    else:
        # first try for a funding year
        
        found_data = funding_year_re.match(office)
        if found_data:
            results = list(found_data.groups())
            funding_year = results[0]
            #print "Got funding year: %s in %s" % (results[0], office)
        else:
            found_data =  congress_no.match(office)
            if found_data:
                results = list(found_data.groups())
                congress = results[0]
            else:
                found_data = fy_re.match(office)
                if found_data:
                    results = list(found_data.groups())
                    #print "fy %s" % (results[0])
                    fiscal_year = results[0]
                else:
                    pass
                    #print "No fy in %s" % (office)
    
    return [senator_name, funding_year, fiscal_year, congress, office]


if __name__ == "__main__":
    import csv
    reader = csv.reader(open("headerlist.csv", 'r'))




    for line in reader:
        office = line[0]
        result = parse_office(office)
        print office
        print result
    
                 