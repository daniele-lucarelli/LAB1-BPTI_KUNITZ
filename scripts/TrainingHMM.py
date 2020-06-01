#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  2 11:02:17 2020

@author: danielelucarelli

Take a csv file with three columns id evalue and label
Derived from an hmm search with a built HMM
Perform a kfold cross-validation and select the best e-value treshold 
for each fold
Print back the report in the standard output

It can be modified to re-use it with other csv files in other projects
It has to be called as:
python3 TrainingHMM.py <csv path> <n of splits>
"""


import sys
import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.model_selection import StratifiedKFold


def create_df(f):
    
    col_names = ["ID", "Evalue", "Label"]
    data = pd.read_csv(f, sep=";", names=col_names)
    return data

def split(data,index, numsplits):
    set_in = next(index)
    data_train = data.iloc[set_in[0]]
    data_test = data.iloc[set_in[1]]
    return data_train, data_test

def comp_ponts(data, thr):
    y_true = data["Label"].values
    y_pred = [1 if (value < thr) else 0 
              for value in data["Evalue"].values]
    confusion = metrics.confusion_matrix(y_true, y_pred, labels=[1, 0])
    ACC = metrics.accuracy_score(y_true, y_pred)
    MCC = metrics.matthews_corrcoef(y_true, y_pred)
    return (confusion, ACC, MCC)

def wrongs_ids(df, thr):
    fn = df.loc[(df["Label"] == 1) & (df["Evalue"] > thr)]
    fp = df.loc[(df["Label"] == 0) & (df["Evalue"] < thr)]
    false = fp, fn
    return false


def thr_try(data,start, stop, step):
    MCCs, exps, ACCs = [], [], []  
    for exp in range(start, stop, step):
        thr = 10 ** exp
        y_true = df["Label"].values
        y_pred = [1 if (value < thr) else 0 for value in df["Evalue"].values]
        MCC = metrics.matthews_corrcoef(y_true, y_pred)
        ACC = metrics.accuracy_score(y_true, y_pred)
        ACCs.append(ACC)
        exps.append(exp)
        MCCs.append(MCC)
        print(thr, ACC, MCC)
    return MCCs, exps, ACCs

def best_thr(data,start, stop, step):
    MCCs, exps, ACCs = thr_try(data, start, stop, step)
    thrs = [10 ** exp for exp in exps]
    best_MCC = 0
    for i in range(len(MCCs)):
        if MCCs[i] > best_MCC:
            best_exp_list = [exps[i]]
            best_MCC = MCCs[i]

    best_exp = np.mean(best_exp_list)
    best_thr = 10 ** best_exp

    return best_thr, thrs, MCCs, ACCs



def train_and_test(data, numsplits):
    report=[]
    false_positives, false_negatives = pd.DataFrame(), pd.DataFrame()
    print("\nSplitting the dataset ", numsplits, "times")
    kfold=StratifiedKFold(n_splits=numsplits,shuffle=True,random_state=40)
    set_index=kfold.split(df, y=df["Label"])
    
    for i in range(numsplits):

        data_train, data_test = split(df, set_index, numsplits)
        b_thr, thr_list, MCC_list, ACC_list= best_thr(data_train,-50,1,1)
        train_point = comp_ponts(data_train, b_thr)
        test_point = comp_ponts(data_test, b_thr)
        report.append((test_point[0], test_point[1], test_point[2], b_thr))
        false = wrongs_ids(data_test, b_thr)       
        false_negatives = pd.concat([false_negatives, false[1]])
        false_positives = pd.concat([false_positives, false[0]])
        print("Fold ", i + 1)
        print("selected threshold",b_thr)
        print("    Training     \tTest ")
        print("ACC", str(train_point[1]), str(test_point[1]))
        print("MCC", str(train_point[2]), str(test_point[2]))
        print("Confusion Matrix train\n", train_point[0])
        print("Confusion Matrix test\n", test_point[0])
        print("\nFalse positives in the test set")
        print(false[0])
        print("\nFalse negatives in the test set")
        print(false[1])
        
    wrong_final = false_positives, false_negatives
    return report, wrong_final







if __name__ == '__main__':
    df=create_df(sys.argv[1])
    train_and_test(df,int(sys.argv[2])
