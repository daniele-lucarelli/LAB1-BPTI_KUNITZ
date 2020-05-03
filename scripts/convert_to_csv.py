#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 18:03:26 2020

@author: danielelucarelli

convert multi column blank separated file into a csv file

called as python3 convert_csv.py <file to be converted> <output>
"""

import sys

def tr(f1,f2):
   f1=open(f1,"r") 
   f2=open(f2,"w")
   for line in f1:
       line=line.replace(" ",";")
       f2.write(line)
   f1.close()
   f2.close()


if __name__ == "__main__":
    tr(sys.argv[1],sys.argv[2])
