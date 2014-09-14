#!/usr/bin/env python
#
# Pull out list of candidate IDs

import pickle
from nltk.corpus import stopwords
import string
from collections import Counter

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words


LANGUAGE = "english"
SENTENCES_COUNT = 10

def process_text(html_text):
    # clear out html
    raw = nltk.clean_html(html_text)
    # now clear out punctuation (requires import string)
    out = raw.translate(string.maketrans("",""), string.punctuation)
    # tokenize
    tokens = nltk.word_tokenize(out.lower())
    # remove stop words
    stop = stopwords.words('english')  # assumes nltk already imported
    tokens = [i for i in tokens if i not in stop]
    print 'Total words %i' % len(tokens)
    print 'Unique words %i' %len(set(tokens))
    return tokens
    
def concat_statements(statIDs):
    stat_list = []
    for stat in statIDs:
    try:
        stat_list.append(mydict[stat])
    except:
        print '%s omitted' % stat
    return ' '.join(jackie_list)
    
def favorite_phrases(tokens):
    cand_bi = nltk.bigrams(tokens)
    return Counter(cand_bi).most_common(8)
    
def clean_text(html_text):
    # clear out html
    raw = nltk.clean_html(html_text)
    nname = ''.join(re.findall('[a-zA-Z0-9.!?(),]?\s?', raw))
    # now clear out punctuation (requires import string)
    #out = raw.translate(string.maketrans("",""), string.punctuation)
    return nname
    
def get_quotes(raw_text):

    parser = PlaintextParser.from_string(clean_text(raw_text), Tokenizer(LANGUAGE))
    # or for plain text files
    # parser = PlaintextParser.from_file("document.txt", Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    
    sentences = []
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        sentences.append(sentence)
    
# Define a main() function
def main():
    # get mapping dict from candidate to statements
    with open('statements_dict.pickle', 'rb') as fh:
        candidate_statements = pickle.load(fh)
    robin = list(candidate_statements['146008'])
    jackie = list(candidate_statements['8425'])
    
    robin_tokens = process_text(concat_statements(robin))
    jackie_tokens = process_text(concat_statements(jackie))
    
    # Get favorite phrases
    robin_fav = favorite_phrases(robin_tokens)
    jackie_fav = favorite_phrases(jackie_tokens)
        
    # Get quotes
    robin_quotes = get_quotes(concat_statements(robin))
    jackie_quotes = get_quotes(concat_statements(jackie))
    

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()