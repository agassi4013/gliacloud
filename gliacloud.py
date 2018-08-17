# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 10:47:16 2018

@author: agassi001
"""
from sklearn.feature_extraction.text import CountVectorizer
import math

def ngram_probs(filename='raw_sentences.txt'):

    with open(filename) as f:
        content = f.readlines()    
        strc = '\n'.join(content)
        strc = strc.lower()
        data_list = strc.strip().split()
        ngram2 = CountVectorizer(ngram_range=(2, 2), decode_error="ignore",
                                        token_pattern = r'\b\w+\b')
        ngram3 = CountVectorizer(ngram_range=(3, 3), decode_error="ignore",
                                        token_pattern = r'\b\w+\b')
        bigram_probs = ngram2.fit_transform(data_list)
        trigram_probs = ngram3.fit_transform(data_list)
        return bigram_probs, trigram_probs
            


cnt2, cnt3 = ngram_probs()
print(cnt2[('we', 'are')])

def prob3(bigram, cnt2=cnt2, cnt3=cnt3):
    prob = cnt3/cnt2[bigram]
    prob = math.log(prob)
    return prob
p = prob3(('we', 'are'))
print(p['family'])