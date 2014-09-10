#!/usr/bin/env python
#
# Pull out list of candidate IDs

import issueRank as ir
import pickle

# Define a main() function
def main():
    # Get a list of candidates currently running for office from VoteSmart
    # Note that this url is for 2014 congressional candidates in the general election
    url = "http://votesmart.org/election/2014/C//2014-congressional?stageId=G&status=8"
    dom = ir.get_dom(url)
    candidate_list = ir.get_candidate_list(dom)
    
    # Pickle the results for future use
    with open('candidate_list.pickle', 'wb') as fh:
        pickle.dump(candidate_list, fh)
    print "number of unique candidate IDs: %i" % len(candidate_list)    

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()