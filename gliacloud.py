# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 10:47:16 2018

@author: agassi001
"""
import math

def ngram_probs(filename='raw_sentences.txt'):
    f = open(filename,'r')
    docs = [line.strip() for line in f.readlines()]

    f.close()

    bigram_probs = dict()
    trigram_probs = dict()
    for line in docs:
        bigram2freqdict(line2bigram(line), bigram_probs)
        trigram2freqdict(line2trigram(line), trigram_probs)
    #print(bigram_probs)
    
    return bigram_probs, trigram_probs


def bigram2freqdict(bigram, bidict):
    for (ch1,ch2) in bigram:
        bidict[(ch1,ch2)]=bidict.get((ch1,ch2),0)+1
    return

def trigram2freqdict(trigram, tridict):
    for (ch1,ch2,ch3) in trigram:
        tridict[(ch1,ch2,ch3)]=tridict.get((ch1,ch2,ch3),0)+1
    return

def line2bigram(mylist):
    words = mylist.lower().split()
    return [words[i:i+2] for i in range(0,len(words)-1)]

def line2trigram(mylist):
    words = mylist.lower().split()
    return [words[i:i+3] for i in range(0,len(words)-2)]


cnt2, cnt3 = ngram_probs()
print(cnt2[('we', 'are')])

def prob3(bigram, cnt2=cnt2, cnt3=cnt3):
    ctwo = cnt2[bigram]
    prob = dict()
    for key in cnt3.keys():
        if bigram[0] == key[0] and bigram[1] == key[1]:
            prob[key[2]]=math.log(cnt3[key]/ctwo)
            #print(key[2])
    return prob

p = prob3(('we', 'are'))
print(p['family'])
