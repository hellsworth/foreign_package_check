This script monitors a set of foreign packages.  
The foreign packages in question are:  
    * lsb  
    * cobbler  
    * open vswitch (ovs)  
    * rabbitmq-server  
    * netfilter-persistent  
    * ipxe  
    * erlang-sd-notify  
This script performs the follow check on each foreign package:  
    * [all] checks the version in the heather repo for the +heather string  
    * [some] grabs the debian/jessie version and checks if it is newer than what is in the heather repo  
In order to run, make sure the following packages are installed: xz-utils, python-dev, liblzma-dev  
Also installed a couple of python modules from these locations:  
    wget => https://pypi.python.org/pypi/wget  
    backports.lzma => https://pypi.python.org/pypi/backports.lzma  
To install the python module, download the .zip file, unpack it, cd to the directory and run:  
    python setup.py install  
