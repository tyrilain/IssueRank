#!/usr/bin/env python

import urllib2, random, time, os, pickle

# set location to save files (on Dropbox for now)
base_folder = os.path.expanduser('~')+'/Dropbox/Insight/votesmart/'
output_folder = os.path.expanduser('~')+'/Dropbox/Insight/votesmart/data/'

##
# This script is to scrape the public statements stored on VoteSmart.org
# Each statement is on a webpage with URL of the form:
#   http://www.votesmart.org/public-statement/[ID number]
# I started with page 917882 on 9/8/14 and am counting backwards.
#
# Author: Tara Lydiard-Martin
# based on a script provided by Brock Mendel
##

def scrape_URLs(URLs, output_folder):
    # Scrape each URL with a short delay between, store in local .html docs
    for URL in URLs:
        with open(output_folder +URL.split('/')[-1]+'.html','wb') as fd:
            try:
                page = urllib2.urlopen(URL)
                fd.write(page.read())
            except:
                print "Failed on: %s" % URL
                # write fails to log file
                with open(base_folder+'log.txt', 'a') as fh:
                    fh.write(URL)
                os.remove(fd.name)

# Define a main() function
def main():

    # Externally store a list of statements that have been scraped
    with open(base_folder+'statements_done.pickle', 'rb') as fh:
        done_statements = pickle.load(fh)
    with open(base_folder+'statements.pickle', 'rb') as fh:
        statements = pickle.load(fh)

    # Calculate statements left to get
    statements_to_get_set = statements - done_statements
    statements_to_get = list(statements_to_get_set)

    print 'Statements to get: %i' % len(statements_to_get)
    
    
    for batch in range(0, len(statements_to_get), 100):
        failed = []
        # Create list of URLs to scrape and put them in random order
        URLs = ['http://www.votesmart.org/public-statement/'+str(x) for x in statements_to_get[batch:batch+100]]
        random.shuffle(URLs)

        # scrape the URLs
        scrape_URLs(URLs, output_folder)

        # save set of scraped statements
        with open(base_folder+'statements_done.pickle', 'wb') as fh:
            dumpme = done_statements.union(set(statements_to_get[batch:batch+100]))
            pickle.dump(dumpme, fh)
        
        print "%i Done" % (batch+100)

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()





