# Senate Disbursements

This is half-done code to parse the senate clerk's report on spending, which are available [here](http://www.senate.gov/legislative/common/generic/report_secsen.htm). 

For more about this project see the introductory blog post [here](https://sunlightfoundation.com/blog/2014/08/05/now-its-easier-to-account-for-how-the-senate-spends-your-money/). 

There's no requirements.txt file, but you'll need pdftotext installed on your system. 

## How to process new files

1. Grab a new file from [here](http://www.senate.gov/legislative/common/generic/report_secsen.htm). You'll want to download the "full report". 
2. Create a new directory to put it in. By convention I've been using  the document number as the dir name, i.e. 114_sdoc4. I think that means that's the fourth document released by the senate clerk's office during the 114th congress. It's absolutely bonkers that the number is that low, of course. God bless the senate for protecting us from any actual data… 
3. In the new directory, copy over rip_pages.py and read_pages.py from the previous files directory. This seems like a crazy thing to do, of course--shouldn't there be code that reads *any* of these files? My experience is that there are sometimes weirdnesses that need some tweaking, and its just easier to keep scripts separate in case you need to rerun them. Also you need to create a "pages" subdirectory, where each of the pages will go. This shouldda been automated, sorry. 
4. Open the "full report" disbursement file and figure out where the "regular" itemizations begin and end. In [this file](http://www.gpo.gov/fdsys/pkg/GPO-CDOC-114sdoc4/pdf/GPO-CDOC-114sdoc4.pdf) the itemizations start on page 17 and end on page 2073. Edit the start_page and end_page to reflect those numbers (they are inclusive). Then run rip_pages (i.e. '$ python rip_pages.py'), which will put a single file for each page in the pages dir. It's looking for pages as a relative file path, so run this script from the directory it's located in. All it does is run pdftotext with the -layout option on one page at a time. 
5. Open read_pages.py and edit the "start_page" and "end_page" on roughly line 225. Again, this couldda been automated, sorry. Then run read_pages from the same directory. It will create two files: "senate_data.csv" and "missing_data.txt". Missing_data.txt is just an array of lines that couldn't be properly parsed. Most of them are lines in the original report that have wrapped in a weird way. More on this in a bit. 
6. Sometimes read_pages.py will freak out and die because there are empty pages between sections in the report. You can just edit the script to exclude these pages. 
7. Running read_pages.py will produce output about problems reading individual lines (it's also dumped to missing_data.txt). These lines are not included in the csv output because they couldn't be properly parsed. Most are "continuations" of lines that are included, so the result is that the description that appears in the csv file is truncated. Others are more complex problems, which may need manual fixes. 