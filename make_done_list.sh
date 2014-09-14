#!/bin/sh

cd ~/Dropbox/Insight/votesmart/data/
ls > ../done.txt
cd ..
perl -pi -e 's/.html//' done.txt

cd ~/Documents/Insight/code/

./make_done_list.py