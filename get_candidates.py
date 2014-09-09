#!/usr/bin/env python

# Functions to extract list of candidates and public statements from VoteSmart

def get_dom(url):
    html_text = requests.get(url).text
    return web.Element(cand_html)

def get_candidate_list(dom):
    # Extract a list of unique candidateIDs on page
    IDs = []
    for cand in dom.by_class('detailscontainer'):
        a =  cand.by_tag('a')[0]    #return element instead of list
        href = a.attributes.get('href', '')
        IDs.append(href.split('/')[2])
        
    myset = set(ID)
    return list(myset)
    
def get_statementIDs(dom):
    # Pull out a list of public-statement IDs from a candidate page
    # Currently just gets landing page (most recent 50, including undated)
    
    # First check whether any statements exist by checking for a notice
    if dom.by_class('notice'):
        return []
    
    # Otherwise, parse page
    IDs = []
    mytable = dom.by_class('article local-details')[0] #should only be one
    for row in mytable.by_tag('tr')[1:]:    #skip first row header
        a = row.by_tag('a')[0]  #return element instead of list
        href = a.attributes.get('href', '')
        IDs.append(href.split('/')[2])
    
    return IDs


# Define a main() function
def main():

    # Get a list of candidates currently running for office from VoteSmart
    # Note that this url is for 2014 congressional candidates in the general election
    url = "http://votesmart.org/election/2014/C//2014-congressional?stageId=G&status=8"
    dom = get_dom(url)
    candidate_list = get_candidate_list(dom)
    
    print "number of unique candidate IDs: %i" % len(candidate_list)
    
    # Try getting a candidate statement list
    candID = 116277
    url = "http://votesmart.org/candidate/public-statements/%i" % candID
    dom = get_dom(url)
    pubstatements = get_statementIDs(dom)
    


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()


