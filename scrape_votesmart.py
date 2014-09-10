#!/usr/bin/env python

import urllib2, random, time, os

##
# This script is to scrape the public statements stored on VoteSmart.org
# Each statement is on a webpage with URL of the form:
#   http://www.votesmart.org/public-statement/[ID number]
# I started with page 917882 on 9/8/14 and am counting backwards.
#
# Author: Tara Lydiard-Martin
# based on a script provided by Brock Mendel
##

# set location to save files (on Dropbox for now)
output_folder = os.path.expanduser('~')+'/Dropbox/Insight/votesmart/'

# Externally store a counter to track how far scraping has gotten
with open('votesmart/counter.txt') as fh:
    counter = int(fh.read())
print 'Counter: %i' % counter



def scrape_URLs(URLs, output_folder):
    # Scrape each URL with a short delay between, store in local .html docs
    for URL in URLs:
        #time.sleep(random.triangular(0.001, 0.1, 0.3))
        with open(output_folder +URL.split('/')[-1]+'.html','wb') as fd:
            try:
                page = urllib2.urlopen(URL)
                fd.write(page.read())
                successful.append(URL)
            except:
                print "Failed on: %s" % URL
                failed.append(URL)
                os.remove(fd.name)

while counter>500000:
    successful = []
    failed = []
    
    # Create list of URLs to scrape and put them in random order
    URLs = ['http://www.votesmart.org/public-statement/'+str(x) for x in range(counter-50,counter)]
    random.shuffle(URLs)
    
    # scrape the URLs
    scrape_URLs(URLs, output_folder)
    
    # write to log
    with open('log.txt', 'a') as fh:
        s = 'Counter %i\n' % counter
        fh.write(s)
        fh.write('Failed:\n')
        for item in failed:
            s = str(item)+'\n'
            fh.write(s)
            
    # update counter
    counter = counter - 50
    with open('votesmart/counter.txt', 'wb') as fh:
        fh.write(str(counter))
    print 'New counter: %i' % counter
    
    time.sleep(random.triangular(1.5, 5, 11))




