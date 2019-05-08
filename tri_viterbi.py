#! /usr/bin/python

# Python port of viterbi.pl

# Usage:  viterbi.py hmm-file < text > tags

import sys, math, re
from collections import defaultdict, deque


hmmfile = sys.argv[1]
textfile = sys.stdin.readlines()

OOV_WORD="OOV"
INIT_STATE="init"
FINAL_STATE="final"

trigram = defaultdict(float)
bigram = defaultdict(float)
unigram	= defaultdict(float)
emissions = defaultdict(float)
tags = defaultdict(int)
vocabs = defaultdict(int)

f = open(hmmfile)

for l in f:
	if l[0] == 't':
		a, b, c, d, e = re.split("\s+", l.rstrip())
		trigram[(b,c,d)] = math.log(float(e))

		tags[b] = 1
		tags[c] = 1
		tags[d] = 1
	elif l[0] == 'e':
		a, b, c, d = re.split("\s+", l.rstrip())
		emissions[(b,c)] = math.log(float(d))
		tags[b] = 1
		vocabs[c] = 1

f.close()

for l in textfile:
	words = re.split("\s+", l.rstrip())
	n = len(words)
	words.insert(0, "")
	V = {}
	Backtrace = {}
	Backtrace[0, INIT_STATE, INIT_STATE] = ''
	V[(0,INIT_STATE,INIT_STATE)] = 0.0
	
	for k in range(1, n+1):
		temp_path = {}

		if words[k] not in vocabs:
			words[k] = OOV_WORD

		for u in tags:
			for v in tags:
				for w in tags:

					if (k-1,w,u) in V and (w,u,v) in trigram and (v,words[k]) in emissions:
						vertex = V[k-1,w,u] + trigram[w,u,v] + emissions[v,words[k]]

						if (k,u,v) not in V or vertex > V[k,u,v]:
							V[k,u,v] = vertex
							Backtrace[k,u,v] = w

	foundgoal = 0
	goal = 0
	for u in tags:
		for v in tags:
			if (n,u,v) in V and (u,v,FINAL_STATE) in trigram:
				
				vertex = V[n,u,v] + trigram[u,v,FINAL_STATE]

				if not foundgoal or vertex > goal:
					goal = vertex
					foundgoal = 1
					u_max = u
					v_max = v

	if foundgoal:
		t = deque()
		t.append(v_max)
		t.append(u_max)

		for i,k in enumerate(range(n-2, 0, -1)):
			t.append(Backtrace[(k+2,t[i+1],t[i])])
		t.reverse()

	if foundgoal:
		print ' '.join(t)
	else:
		print ''