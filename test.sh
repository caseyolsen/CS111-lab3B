#!/bin/bash
for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22
do
    curl -s http://web.cs.ucla.edu/classes/cs111/Samples/P3B-test_$i.csv -o test$i.csv
    echo === RUNNING TEST $i ===
    echo test result:
    python3 lab3b.py test$i.csv
    echo provided result:
    curl -s http://web.cs.ucla.edu/classes/cs111/Samples/P3B-test_$i.err
    rm -f test$i.csv
    echo
done
