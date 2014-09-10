#!/usr/bin/env python

# Functions to extract list of candidates and public statements from VoteSmart

import requests
from pattern import web

def get_dom(url):
    html_text = requests.get(url).text
    return web.Element(html_text)

def get_candidate_list(dom):
    # Extract a list of unique candidateIDs on page
    IDs = []
    for cand in dom.by_class('detailscontainer'):
        a =  cand.by_tag('a')[0]    #return element instead of list
        href = a.attributes.get('href', '')
        IDs.append(href.split('/')[2])
        
    myset = set(IDs)
    return list(myset)

def parse_IDs(dom):
    # Parse IDs from page
    IDs = []
    mytable = dom.by_class('article local-details')[0] #should only be one
    for row in mytable.by_tag('tr')[1:]:    #skip first row header
        a = row.by_tag('a')[0]  #return element instead of list
        href = a.attributes.get('href', '')
        IDs.append(href.split('/')[2])
    return IDs
    
def get_last_page(dom):
    mydiv = dom.by_class('pagination')[0]  #use first
    mylink = mydiv.by_tag('li')[-1]  #want last link
    a = mylink.by_tag('a')[0]
    href = a.attributes.get('href', '')
    return href

def get_statementIDs(dom):
    # Pull out a list of public-statement IDs from a candidate page
    # Currently just gets landing page (most recent 50, including undated)
    
    IDs = []
    
    # First check whether any statements exist by checking for a notice
    if dom.by_class('notice'):
        return []
    # Check if have multiple pages
    if not dom.by_class('pagination'):
        IDs.extend(parse_IDs(dom))
    else:
        link_struct = "http://votesmart.org"+get_last_page(dom)  #returns a string
        base_link = link_struct.split('=')
        last_page = int(base_link[-1])  #store last page
        base_link = base_link[:-1]  #store list of url parts minus page number

        for page in range(1,last_page+1):
            url = '='.join(base_link)+'='+str(page)
            dom = get_dom(url)
            IDs.extend(parse_IDs(dom))

    return (set(IDs))


# Define a main() function
def main():

    # Get a list of candidates currently running for office from VoteSmart
    # Note that this url is for 2014 congressional candidates in the general election
    url = "http://votesmart.org/election/2014/C//2014-congressional?stageId=G&status=8"
    dom = get_dom(url)
    candidate_list = get_candidate_list(dom)
    with open('candidate_list.txt', 'a') as fh:
        for item in candidate_list:
            s = str(item)+'\n'
            fh.write(s)
    
    print "number of unique candidate IDs: %i" % len(candidate_list)
    
    # Try getting a candidate statement list
    #candID = 116277
    #url = "http://votesmart.org/candidate/public-statements/%i" % candID
    #dom = get_dom(url)
    #pubstatements = get_statementIDs(dom)
    
    # Iterate over all candidates to build dictionary
    #statementIDs = []
    #for candID in candidate_list:
    #    url = "http://votesmart.org/candidate/public-statements/%i" % candID
    #    dom = get_dom(url)
    #    statementIDs.extend(get_statementIDs(dom))
    #    
    #uniqueStatements = set(statementIDs)
    

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()


