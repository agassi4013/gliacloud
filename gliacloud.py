# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 10:47:16 2018

@author: agassi001
"""
import math
from heapq import nlargest

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

def predict_max(starting, cnt2=cnt2, cnt3=cnt3):
    searchw = starting
    list_of_words = [starting[0], starting[1]]
    while list_of_words[-1] != '.' and len(list_of_words)<16:
        pws = prob3(searchw)
        pw_k = list(pws.keys())
        pw_v = list(pws.values())
        nextw = pw_k[pw_v.index(max(pw_v))]
        list_of_words.append(nextw)
        searchw = (searchw[1],nextw)
        #print(nextw)
    return list_of_words

sent = predict_max(('we', 'are'))
assert sent[-1] == '.' or len(sent) <= 15
print(' '.join(sent))

def predict_beam(bigram, beam_size=4, sent_length=10, cnt2=cnt2, cnt3=cnt3):    
    #list_of_sentence = []
    list_of_words = [bigram[0], bigram[1]]
    slist = [list_of_words]
    sdict=dict()
    for i in range(len(bigram),sent_length-2):
        dictrun=dict()
        for s in slist:
            if ' '.join(s) in sdict.keys():
                preprob = sdict[' '.join(s)]
            else:
                preprob = 0
            searchw = (s[-2],s[-1])
            p3search = prob3(searchw)
            larg4 = nlargest(beam_size, p3search, key = p3search.get)
            for l in larg4:
                if l != '.':
                    sl = s+[l]
                    dictrun[' '.join(sl)] = p3search[l]+preprob
        larg4of16 = nlargest(beam_size, dictrun, key = dictrun.get)
        li = [line.split(' ') for line in larg4of16]
        slist = li
        sdict = dictrun
    #print(slist)
    dictrun=dict()
    for s in slist:
        preprob = sdict[' '.join(s)]
        searchw = (s[-2],s[-1])
        p3search = prob3(searchw)
        pk = p3search.keys()
        for k in pk:
            if k != '.':
                sk = s+[k]
                pprob = preprob+p3search[k]
                searchw = (s[-1],k)
                fsearch = prob3(searchw)
                if '.' in fsearch.keys():
                    dictrun[' '.join(sk)] = fsearch['.']+pprob
    
    last4 = nlargest(beam_size, dictrun, key = dictrun.get)
    #print(last4)
    list_of_sentence = [line.split(' ')+['.'] for line in last4]    
        
    return list_of_sentence

#predict_beam(('we', 'are'))
for sent in predict_beam(('we', 'are')):
    assert sent[-1] == '.' or len(sent) < 10
    print(' '.join(sent))