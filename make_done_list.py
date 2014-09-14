#!/usr/bin/env python
#
# Regenerate list of scraped statements
# First run ls>../done***.txt and cut off the .html using perl

import pickle
import os

base_folder = os.path.expanduser('~')+'/Dropbox/Insight/votesmart/'

with open(base_folder+'done.txt', 'rb') as fh:
    done_text = fh.read()

done_list = done_text.split()

with open(base_folder+'statements_done.pickle', 'wb') as fh:
    dumpme = set(done_list)
    print '%i Done' % len(dumpme)
    pickle.dump(dumpme, fh)