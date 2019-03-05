# NAME: Casey Olsen,Kenna Wang
# ID: 004938486,604939143
# EMAIL: casey.olsen@gmail.com,kenna.wang6@gmail.com


.SILENT:

default:
	rm -f lab3b
	ln -s lab3b.py lab3b
	chmod +x lab3b
#	python3 lab3b.py trivial.csv

clean:
	rm -f *.tar.gz lab3b

dist: 
	tar -czvf lab3b-004938486.tar.gz README Makefile lab3b.py
