#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 18:03:26 2020

@author: danielelucarelli

take the id column from a blast file and retrieve the ids
 
than iterate in a fasta file and retrieve the matches

than print the matches to another file


It has to be called as:
python3 get_blast_id_retrieve sequences  <blast file>  <fasta file>  <output file> <integer with the column to extract from blast file>

"""


import sys

def get(f1):
    filein=open(f1,"r")
    id_li=[]
    for line in filein:
     
     id_li.append(line.rstrip())
    filein.close()
    return id_li

def get_seq(f2,id_li):
    filein=open(f2,"r")
    content=filein.read()
    seqs=content.split('>')
    seqs.remove("")
    print (seqs)
    for i in seqs:
        if i[3:9] not in id_li:
            seqs.remove(i)
 			
    
    return seqs
        


if __name__=='__main__':
    x=int (sys.argv[4])-1
    id_li = get(sys.argv[1])
    seqs=get_seq(sys.argv[2],id_li)
    f3= open(sys.argv[3], "w")
    print (len(seqs))
    print(len(id_li))
    for i in seqs:
        f3.write('>' + i)
    f3.close()
