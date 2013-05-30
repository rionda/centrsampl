#! /usr/bin/env python3
# -*- coding: iso-8859-1 -*-
"""compare.py

Compare estimations of betweenness centralities to exact values. 

"""
import argparse
import itertools
import logging
import math
import os.path
import pickle

import converter
import util


def comparison_exact(method,path,point,number_runs,metric):
    #metric: euclid_dist, absolute_deviation, inversions

    sum_over_runs=0;

    pkl_file = open(path+'/out_files/out_exact'+'_'+str(point)+'.picklez','rb')
    reader_1 = pickle.load(pkl_file)
    exact_betw = reader_1[1][0][1]
   
    pkl_file = open(path+'/out_files/out_'+method+'_'+str(point)+'.picklez','rb')
    reader_2 = pickle.load(pkl_file)


    for i in range(0,int(number_runs)-1):

  #reader[1] is the 'results' from *_experiment
	#reader[1][1] is the betw 
	#reader[1][1][j] is the betweness of the jth run
        inv_count = 0

        approx_betw = reader_2[1][int(i)][1]
  
        if metric == 'euclid_dist':  
          sum_over_runs = sum_over_runs + math.sqrt(sum([math.pow(a - b, 2) for a,b in zip(exact_betw,approx_betw)]))
        elif metric == 'absolute_deviation':
          sum_over_runs = sum([abs(a - b) for a,b in zip(exact_betw,approx_betw)])
	#Slow and dirty O(n^2) version
	#Considering increasing ranking
        elif metric == 'inversions':
          ranks_exact = sorted(range(len(exact_betw)), key=exact_betw.__getitem__)
          ranks_approx = sorted(range(len(approx_betw)), key=approx_betw.__getitem__)
          for j in range(0,len(ranks_exact)-1):
            inv_count= inv_count + abs(ranks_exact.index(j)-ranks_approx.index(j)) 
            #print(inv_count)
            ranks_approx.remove(j)
            ranks_approx.insert(ranks_exact.index(j),j)
          sum_over_runs = sum_over_runs + inv_count   

 
    ret_val = sum_over_runs / int(number_runs)
    print(ret_val)


def main():
    """Parse arguments, do the comparison, write to output."""
    parser = argparse.ArgumentParser()
    parser.add_argument("method", help="the methods vc,bp,gss")
    parser.add_argument("path", help="the point/run of the method vc,bp,gss")
    parser.add_argument("point", help="the point of the method vc,bp,gss")   
    parser.add_argument("number_runs", help="the number of runs of the method vc,bp,gss")   
    parser.add_argument("metric", help="one of the metrics euclid_dist,absolute_deviation,inversions")
    args = parser.parse_args()
     
     
    comparison_exact(args.method,args.path,args.point,args.number_runs,args.metric) 
     

    #math.sqrt(sum([math.pow(a - b, 2) for a,b in zip(norm_exact_betw,norm_vc_betw)]))
    
        
if __name__ == "__main__":
  main()

