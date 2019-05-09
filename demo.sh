#!/bin/bash


for ((i=1;i<101;i++))
do
	count=$(($i*400))
	echo "$count"
	./train_hmm_modified.py ptb.2-21.tgs ptb.2-21.txt $count > mytest.hmm
	./viterbi.pl mytest.hmm < ptb.22.txt > mytest.out
	./tag_acc.pl ptb.22.tgs mytest.out
	rm mytest.out
	rm mytest.hmm
done
