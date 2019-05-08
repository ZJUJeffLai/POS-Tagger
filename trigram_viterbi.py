# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 01:42:09 2019
Python2.7
@author: JeffLai @ UC Davis
"""
import math
import sys
import re
from collections import defaultdict
from collections import deque

# hmmfile
HMM_FILE = sys.argv[1]
TEXT_FILE = sys.stdin.readlines()

# Special keywords
INIT_STATE = "init"
FINAL_STATE = "final"
OOV_SYMBOL = "OOV"

emissions= defaultdict(float)
trigram = defaultdict(float)
tag = defaultdict(int)
vocab = defaultdict(int)

f = open(HMM_FILE)

for ff in f:
    if ff[0] == 't':
        q1,q2,q3,q4,q5 = re.split("\s+",ff.rstrip())
        trigram[(q2,q3,q4)] = math.log(float(q5))
        tag[q2] = 1
        tag[q3] = 1
        tag[q4] = 1
    elif ff[0] == 'e':
        q1,q2,q3,q4 = re.split("\s+",ff.rstrip())
        emissions[(q2,q3)] = math.log(float(q4))
        tag[q2] = 1
        vocab[q3] = 1
f.close()

## read in one sentence at a time
for s in TEXT_FILE:
    # @w = split;
    w = re.split("\s+",s.rstrip())
    # $n = scalar(@w)
    n = len(w)
    # unshift @w, ""
    w.insert(0,"")
    # %V = ()
    V = {}
    # Backtrace = ();
    Backtrace = {}
    Backtrace[0,INIT_STATE,INIT_STATE] = ''
    V[(0,INIT_STATE,INIT_STATE)] = 0.0
    for i in range(1,n+1):
        # if a word isn't in the vocabulary, rename it with the OOV symbol
        if w[i] not in vocab:
            w[i] = OOV_SYMBOL
        for t in tag:
            for tt in tag:
                for ttt in tag:
                    if (i-1,ttt,t) in V and (ttt,t,tt) in trigram and\
                    (tt,w[i]) in emissions:
                        viterbi = V[i-1,ttt,t]+trigram[ttt,t,tt]+emissions[tt,w[i]]
                        #if(!(defined $V{$i}{$q}) or $v > $V{$i}{$q}) 
                        if (i,t,tt) not in V or viterbi > V[i,t,tt]:
                            V[i,t,tt] = viterbi
                            Backtrace[i,t,tt] = ttt
    foundgoal = 0
    goal = 0
    for Q1 in tag:
        for Q2 in tag:
            if(n,Q1,Q2) in V and (Q1,Q2,FINAL_STATE) in trigram:
                viterbi = V[n,Q1,Q2]+trigram[Q1,Q2,FINAL_STATE]
                #if(!$foundgoal or $v > $goal)
                if not foundgoal or viterbi > goal:
                    goal = viterbi
                    foundgoal = 1
                    Q1_max = Q1
                    Q2_max = Q2
    
    if foundgoal:
        t = deque()
        t.append(Q2_max)
        t.append(Q1_max)
        for i,j in enumerate(range(n-2,0,-1)):
            t.append(Backtrace[(j+2,t[i+1],t[i])])
        t.reverse()
    if foundgoal:
        print ' '.join(t)
    else:
        print ''
    

