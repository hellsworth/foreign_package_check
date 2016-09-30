#!/usr/bin/env python

from commands import *
import re
import json
import wget
import os
import backports.lzma

'''
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
    * [some] grabs the debian/jessie version and checks if it is newer than what is in
    the heather repo

In order to run, make sure the following packages are installed: xz-utils,
python-dev, liblzma-dev

Also installed a couple of python modules from these locations:
    wget => https://pypi.python.org/pypi/wget
    backports.lzma => https://pypi.python.org/pypi/backports.lzma
To install the python module, download the .zip file, unpack it, cd to the directory and run:
    python setup.py install
'''

def get_package_versions(pkg, url, newname):
    '''
    This function takes the dictionary of packages names (keys) and populates the corresponding package versions (values) found in the relevent Packages.xz. In order to access the Packages.xz file, it is first retrieved and the name is changed to something unique since this function will generally be used multiple times.
    '''
    packages_xz = wget.download(url)
    print "\n"
    os.rename('Packages.xz', newname)
    with backports.lzma.open(newname) as f:
        searchlines = f.readlines()
    f.close()
    os.remove(newname)
    for key in pkg:
        package_line = 'Package: %s\n' % key
        for i, line in enumerate(searchlines):
            if package_line in line:
                for l in searchlines[i:i+3]:
                    ver = re.match(r'Version:\s+(\S+)', l)
                    if ver is not None:
                        pkg[key] = ver.group(1)
    return pkg

def populate_fp_dict(pkg, pkg_file):
    '''
    Based on an input text file that contains a list of foreign packages, this function creates a dictionary to be used as a template where each key is a foreign package and the value is set to None.
    '''
    f = open(pkg_file,'r')
    searchlines = f.readlines()
    f.close()
    for i, line in enumerate(searchlines):
        pkg.setdefault(line.rstrip('\n'),[]).append(None)
    return pkg

def look_for_heather(heather_pkg):
    '''
    This function simply checks foreign packages for the heather string because it should be there.
    '''
    for i in heather_pkg:
        regexp = re.compile(r'\+heather')
        if regexp.search(heather_pkg[i]) is not None:
            continue
        else:
            print "== ERROR: {} is missing the heather string!".format(i)
            print "%s => %s" % (i, heather_pkg[i])

def ovs_compare():
    
    


if __name__ == '__main__':

    # heather_url points to some url to a Packages.xz file of the repo that you want to compare to
    # heather_url = </path/to/Packages.xz>

    jessie_url = 'http://ftp.us.debian.org/debian/dists/jessie/main/binary-amd64/Packages.xz'
    stretch_url = 'http://ftp.us.debian.org/debian/dists/stretch/main/binary-amd64/Packages.xz'
    sid_url = 'http://ftp.us.debian.org/debian/dists/sid/main/binary-amd64/Packages.xz'

    # Populate the base dictionary with foreign package keys and None as the version
    pkg = {}
    pkg_file = 'my_foreign_packages.txt'
    populate_fp_dict(pkg,pkg_file)

    # Populate the heather dictionary with foreign package keys and the version that is in the heather TOT repo
    heather_pkg = pkg.copy()
    print "Getting heather packages"
    heather_pkg = get_package_versions(heather_pkg, heather_url, 'heather_packages.xz')

    print "\n=== heather packages ==="
    for y in heather_pkg:
        print "{:<25} {:<25}".format(y, heather_pkg[y])

    # Perform the check for the 'heather' string in the heather foreign package versions
    look_for_heather(heather_pkg)
   
    # Populate the jessie dictionary with foreign package keys and the version that is in the debian/jessie repo
    jessie_pkg = pkg.copy()
    print "\nGetting jessie packages"
    jessie_pkg = get_package_versions(jessie_pkg, jessie_url, 'jessie_packages.xz')

    print "\n=== jessie packages ==="
    for w in jessie_pkg:
        print "{:<25} {:<25}".format(w, jessie_pkg[w])

    # Populate the stretch dictionary with foreign package keys and the version that is in the debian/stretch repo
    stretch_pkg = pkg.copy()
    print "\nGetting stretch packages"
    stretch_pkg = get_package_versions(stretch_pkg, stretch_url, 'stretch_packages.xz')

    print "\n=== strech packages ==="
    for q in stretch_pkg:
        print "{:<25} {:<25}".format(q, stretch_pkg[q])

    # Populate the sid dictionary with foreign package keys and the version that is in the debian/sid repo
    sid_pkg = pkg.copy()
    print "\nGetting sid packages"
    sid_pkg = get_package_versions(sid_pkg, sid_url, 'sid_packages.xz')

    print "\n=== sid packages ==="
    for r in sid_pkg:
        print "{:<25} {:<25}".format(r, sid_pkg[r])


