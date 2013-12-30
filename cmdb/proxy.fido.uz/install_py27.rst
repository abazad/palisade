******************
Install Python 2.7
******************
1. Install prerequisite packages::
	
	yum install bzip2-devel openssl-devel sqlite-devel readline-devel

2. Download&Install Python2.7::
	
	wget -c http://python.org/ftp/python/2.7.6/Python-2.7.6.tgz
	tar -xvzf Python-2.7.6.tgz 
	cd Python-2.7.6
	./configure --prefix=/usr/local
	make
	sudo make altinstall

2. Download and install PIP::
	
	wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
	wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py	
	sudo /usr/local/bin/python2.7 ez_setup.py 
	sudo /usr/local/bin/python2.7 get-pip.py
   

Make log
========

Python build finished, but the necessary bits to build these modules were not found:
_bsddb             _tkinter           bsddb185        
dbm                gdbm               sunaudiodev   