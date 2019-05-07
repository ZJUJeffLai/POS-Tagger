# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 20:33:53 2019
Python3.7
@author: JeffLai @ UC Davis
"""

import math
import sys
import re
from collections import defaultdict

# hmmfile
HMM_FILE = sys.argv[1]
TEXT_FILE = sys.stdin.readlines()

# Special keywords
INIT_STATE = "init"
FINAL_STATE = "final"
OOV_SYMBOL = "OOV"

emissions={}
transitions={}
tag = defaultdict(int)
vocab = defaultdict(int)

f = open(HMM_FILE)

for ff in f:
    q1,q2,q3,q4 = re.split("\s+",ff.rstrip())
    
    if q1 == 'trans':
        if q2 not in transitions:
            transitions[q2] = defaultdict(float)
        #$A{$qq}{$q} = log($p);
        transitions[q2][q3] = math.log(float(q4))
        #$States{$qq} = 1;
        #ates{$q} = 1;
        tag[q2] = 1
        tag[q3] = 1
#close(HMM);
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
    # V{0}{$init_state} = 0.0
    V['0'] = defaultdict(float)
    V['0'][INIT_STATE] = 0.0
    
    for i in range(n+1):
        # if a word isn't in the vocabulary, rename it with the OOV symbol
        if w[i] not in vocab:
            w[i] = OOV_SYMBOL
        if str(i) not in V:
            V[str(i)] = defaultdict(float)
        if str(i) not in Backtrace:
            Backtrace[str(i)] = defaultdict(str)
        
        #foreach $q (keys %States) { # consider each possible current state
		#foreach $qq (keys %States) { # each possible previous state
        for t in tag:
            for tt in tag:
                #if(defined $A{$qq}{$q}  # only consider "non-zeros"
				#and defined $B{$q}{$w[$i]} 
				#and defined $V{$i - 1}{$qq}
                if tt in transitions and t in transitions[tt] and t in emissions and\
                w[i] in emissions[t] and str(i-1) in V and tt in V[str(i-1)]:
                    #$v = $V{$i - 1}{$qq} + $A{$qq}{$q} + $B{$q}{$w[$i]}
                    viterbi = V[str(i-1)][tt] + transitions[tt][t] + emissions[t][w[i]]
                    #if(!(defined $V{$i}{$q}) or $v > $V{$i}{$q}) 
                    if(q not in V[str(i)]) or viterbi > V[str(i)][t]:
                        # if we found a better previous state, take note!
						#$V{$i}{$q} = $v;  # Viterbi probability
						#$Backtrace{$i}{$q} = $qq; # best previous state
                        V[str(i)][t] = viterbi
                        Backtrace[str(i)][t] = tt
    foundgoal = 0
    goal = 0
    for qq in tag:
        #if(defined $A{$qq}{$final_state} and defined $V{$n}{$qq})
        if qq in transitions and FINAL_STATE in transitions[qq] and\
        str(n) in V and qq in V[str(n)]:
            #if(!$foundgoal or $v > $goal)
            if not foundgoal or viterbi > goal:
                goal = viterbi
                foundgoal = 1
                q = qq
    if foundgoal:
        t = []
        for i in range(n,0,-1):
            t.insert(0,q)
            q = Backtrace[str(i)][q]
    if foundgoal:
        print ' '.join(t)
    else:
        print ''
                    
                    
                   
                        
                    
                
                    
    


