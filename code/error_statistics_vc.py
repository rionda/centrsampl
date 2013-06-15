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
import operator


def error_statistics_vc(path,point,number_runs):
    #metric: euclid_dist, absolute_deviation, inversions   


   pkl_file = open(path+'/out_files/out_exact_1.picklez','rb')
   reader_1 = pickle.load(pkl_file)
   exact_betw = reader_1[1][0][1]
   data={}

   sum_over_runs=[]

   for i in range(0,len(exact_betw)):
      sum_over_runs.append(0)


   pkl_file = open(path+'/out_files/out_vc_'+str(point)+'.picklez','rb')
   reader_2 = pickle.load(pkl_file)

      #sum_over_runs=[0,0,0,0,0]
      #exact_betw=[1, 1, 1, 1, 1]
   average=0
   stddev=0
   maximum=0

   for i in range(0,int(number_runs)-1):
      approx_betw = reader_2[1][int(i)][1]
        #approx_betw=[2, 2, 2, 2, 2]   
      error_run = [ abs(a - b) for a,b in zip(exact_betw,approx_betw)]
      temp_avg = sum(error_run)/(len(error_run)*1.0)
      average = average + temp_avg
      temp_stddev =  [ pow(x-temp_avg,2) for x in error_run ]
      stddev = stddev +  pow((1/len(error_run))*sum(temp_stddev),1/2)
      temp_max = max(error_run)
      if temp_max > maximum:
       maximum = temp_max
   #name='run_'+ str(point)
   #data[name] = sum_over_runs
   #print(data) 
   #scipy.io.savemat('vc_diff_'+point+'.mat',data)
   print(average)
   print(stddev)
   print(maximum)

def main():
    """Parse arguments, do the comparison, write to output."""
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="the point/run of the method vc")
    parser.add_argument("point", help="the point of the method vc runs")
    parser.add_argument("number_runs", help="the total number of runs of the method vc runs")
    args = parser.parse_args()


    error_statistics_vc(args.path,args.point,args.number_runs)


if __name__ == "__main__":
  main()
