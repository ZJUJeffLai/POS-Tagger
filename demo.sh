#!/bin/sh


for ((i=1;i<101;i++))
do
	count=$(($i*400))
	echo "$count"
	./train_hmm_modified.py ptb.2-21.tgs ptb.2-21.txt $count > my.hmm
	./viterbi.pl my.hmm < ptb.22.txt > my.out
	./tag_acc.pl ptb.22.tgs my.out
	rm my.out
	rm my.hmm
done
