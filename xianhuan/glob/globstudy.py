#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
for root,dirs,files in os.walk("/Users/cxhuan/Downloads/globtest/hello"):
    for dir in dirs:
        print(os.path.join(root, dir))
    for file in files:
        print(os.path.join(root, file))

import os
files = list()
def dirAll(pathname):
    if os.path.exists(pathname):
        filelist = os.listdir(pathname)
        for f in filelist:
            f = os.path.join(pathname, f)
            if os.path.isdir(f):
                dirAll(f)
            else:
                dirname = os.path.dirname(f)
                baseName = os.path.basename(f)
                if dirname.endswith(os.sep):
                    files.append(dirname+baseName)
                else:
                    files.append(dirname+os.sep+baseName)

dirAll("/Users/cxhuan/Downloads/globtest/hello")
for f in files:
    print(f)

import glob
import os

for p in glob.glob('/Users/cxhuan/Downloads/globtest/*'):
    print(p)

print('----------------------')

for p in glob.glob('/Users/cxhuan/Downloads/globtest/*/*'):
    print(p)

print('----------------------')

for p in glob.glob('/Users/cxhuan/Downloads/globtest/hello/*3.txt'):
    print(p)

print('----------------------')

for p in glob.glob('/Users/cxhuan/Downloads/globtest/hello/hello?.txt'):
    print(p)

print('----------------------')

for p in glob.glob('/Users/cxhuan/Downloads/globtest/hello/*[0-2].*'):
    print(p)

print('----------------------')

p = glob.glob('/Users/cxhuan/Downloads/globtest/hello/hello?.*')
print(p)

print('----------------------')

p = glob.iglob('/Users/cxhuan/Downloads/globtest/hello/hello?.*')
print(p)
print(p.__next__())
print(p.__next__())


