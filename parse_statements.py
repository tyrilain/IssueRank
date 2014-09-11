#!/usr/bin/env python
#
# Pull out list of candidate IDs

#import issueRank as ir
import pickle, time, string
import os, sys
import pymysql as mdb 
from pattern import web

# set location to save files (on Dropbox for now)
base_folder = os.path.expanduser('~')+'/Dropbox/Insight/votesmart/'
data_folder = os.path.expanduser('~')+'/Dropbox/Insight/votesmart/data/'

# for removing punctuation from date strings later
remove_punct_map = dict.fromkeys(map(ord, string.punctuation))

# this establishes the connection to the database
# you'll need to update the password field
conn = mdb.connect(host='localhost',port=int(3306),user='root',db='VoteSmart')  #,passwd='YOUR_PASSWORD_HERE'
x = conn.cursor()

def parse_page(ID):
    # Open html file
    with open(data_folder+ID+'.html', 'rb') as fh:
        html_text = fh.read()

    # Convert to dom and extract relevant fields
    dom = web.Element(html_text)
    dom = dom.by_class("header clearfix")[0]
    title = dom.by_attr(itemprop="name")[0].content
    date = dom.by_attr(itemprop="datePublished")[0].content
    locale = dom.by_attr(itemprop="contentLocation")[0].content
    article = dom.by_attr(itemprop="articleBody")[0].content

    # Convert date format (remove punctuation, then convert to standard format)
    initial_date = date.translate(remove_punct_map)
    # need to make sure only have 3 letter month code (June causes problems)
    temp = initial_date.split()
    clean_date = ' '.join([temp[0][:3], temp[1], temp[2]])
    # convert to time object then back to pretty string
    out = time.strptime(clean_date, "%b %d %Y")
    date = time.strftime("%Y-%m-%d", out)
    
    return (ID, title, date, locale, article)

def store_sql(row_entry):
    # Write to SQL statements_tbl (need to have already opened connection)
    # this is the command I want to send MySQL with variables which I can fill in later
    insert = '''
      INSERT into statements_tbl 
      (id, title, date, location, article) 
      VALUES (%s,%s,%s,%s,%s)
      '''
    # this sends the cammand, with a set of variables that I choose
    x.execute(insert,row_entry)
    # so far everything that's been done is held in a temporary space. This command makes it permenant.
    # without this command, the changes to the database will dissapear once the script finished running
    conn.commit()
    


    
# Define a main() function
def main():
    
    parsed = []
    failed = []
    
    # Iterate through IDs to parse
    with open(base_folder+'done0910_8pm.txt', 'rb') as fh:
        filelist = fh.read()
        IDs = filelist.split()
        
    for ID in IDs:
#         row_entry = parse_page(ID)
#         print ID
        try:
            row_entry = parse_page(ID)
            store_sql(row_entry)
            # Store list of finished files
            parsed.append(ID)
            print ID
        except:
            e = sys.exc_info()[0]
            print "<p>Error: %s</p>" % e
            failed.append(ID)
            print 'failed: %s' % ID
            
    
    # you should close the session when you finish
    x.close()
    conn.close()
    
    
    
# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()