# NAME: Casey Olsen
# ID: 004938486
# EMAIL: casey.olsen@gmail.com


.SILENT:

#default:#
#	python3 lab3b.py trivial.csv

clean:
	rm -f *.tar.gz lab3b

dist: 
	tar -czvf lab3b-004938486.tar.gz README Makefile lab3b.py
