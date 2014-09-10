#!/usr/bin/env python

import issueRank as ir
import pickle

# Define a main() function
def main():
   
    
    #Try getting a candidate statement list
    #candID = 116277
    #url = "http://votesmart.org/candidate/public-statements/%i" % candID
    #dom = get_dom(url)
    #pubstatements = get_statementIDs(dom)
    
    # Read in candidate list from file
    with open('candidate_list.pickle', 'rb') as fh:
        candidate_list = pickle.load(fh)
    
    print 'total number of candidates: %s' % len(candidate_list)
    #print 'first: %s' % candidate_list[0]
    #print 'last: %s' % candidate_list[-1]
    
    # Iterate over all candidates to build dictionary
    # load the ones we've already pickled
    with open('statements_dict.pickle', 'rb') as fh:
        candidate_statements = pickle.load(fh)
    print 'number of candidates stored: %s' % len(candidate_statements)
    candidate_list = candidate_list - set(candidate_statements.keys())
    print 'number of candidates remaining: %s' % len(candidate_list)
    
    with open('statements.pickle', 'rb') as fh:
        statementIDs = pickle.load(fh)
    #candidate_statements = {}
    #statementIDs = set([])

    
    for candID in candidate_list:
        print 'candID %s' % candID
        url = "http://votesmart.org/candidate/public-statements/%s" % candID
        dom = ir.get_dom(url)
        statements = ir.get_statementIDs(dom)
        
        candidate_statements[candID] = statements
        statementIDs.update(statements)
        with open('statements.pickle', 'wb') as fh:
            pickle.dump(statementIDs, fh)
        with open('statements_dict.pickle', 'wb') as fh:
            pickle.dump(candidate_statements, fh)
    
    print 'There are %i public statements.' % len(statementIDs)
    

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()