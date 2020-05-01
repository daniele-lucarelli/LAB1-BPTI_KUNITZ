#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 18:39:56 2020

@author: danielelucarelli

take a fasta file and split into n fasta files 
has to be called as: python3 split-fasta-random.py <file to split> <n of times has to be splitted> <string to add at the beginning of the output files'name>

"""


import sys
import random as rd

def count_seq(f):

    with open(f,'r') as file:
        c=0
        for line in file:
            if '>' in line:
                c+=1
        return c

def cr_f(n):

    files=[]
    n=int(n)
    for i in range(1,n+1):
        if sys.argv[3]=="":
            files.append(sys.argv[1]+ str(i))
        else:
            files.append(sys.argv[3]+ sys.argv[1]+ str(i))
    return files
    
    

def split (f1,n,l):

     file=open(f1,"r")   
     f=file.read()
    
     files=[]
     f_o=''
     l=l//int(n)
     for line in f:
         if line.startswith('>'):             
             files.append(f_o)
             f_o=""
             f_o+=line                            
         else:
             f_o+=line                                        
     files.append(f_o)
     files.remove("")
     return files
 
    
    
if __name__=='__main__':
    files=split(sys.argv[1],sys.argv[2],count_seq(sys.argv[1]))
    n=sys.argv[2]
    create=cr_f(n)
    rd.shuffle(files)
    files = [files[x:x+((len(files))//int(n))] for x in range(0,len(files),(len(files))//int(n))]
    
    for a,b in zip(files,create):
       f=open(b,"w")
       
       s="\n".join(a)
       f.write(s)
    
