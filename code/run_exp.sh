#
#
# $1 should be the graph dataset for the experiment
# $2 should be either -u or -d
# Y-axis: time, err_avg, touched_edges
#  X-axis: samples
# We create a out.txt that keeps track of all the data
#

# Check whether the file exists
if ! [ -f /data/people/matteo/centrsampl/$1 ]
then 
  echo -e "\n File $1, is not at directory /data/people/matteo/centrsampl/"
fi


dataset=${1/\.*}

#Create a new directory, use the pid in order to avoid  overwriting a useful run
mkdir ./${dataset}_fixedSample_$$
path=./${dataset}_fixedSample_$$

no_nodes=$(python3 number_nodes.py /data/people/matteo/centrsampl/$1)

#Compute the different sample sizes

#percentages_val="0.01 0.05 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45"
percentages_val="0.01 0.05"
percentages=($percentages_val)
number_point=${#percentages[@]}

#Initialize the X-axis (number of samples)
echo "X = ["  > $path/X.txt
iter=0
while [ $iter -le $number_point ]
do
  echo "${percentages[$iter]} * $no_nodes" | bc -l >> $path/X.txt
  (( iter += 1 ))
done
echo "];"  >> $path/X.txt


# Each run for a fixed sample size is repeated $repetitions and averaged.
repetitions_4_each_point=2


#Initialize the files
echo "Y_vc_time = ["  > $path/Y_vc_time.txt
echo "Y_bp_time = ["  > $path/Y_bp_time.txt
echo "Y_gss_time = ["  > $path/Y_gss_time.txt
echo "Y_exact_time = ["  > $path/Y_exact_time.txt

echo "Y_vc_err_avg = ["  > $path/Y_vc_err_avg.txt
echo "Y_bp_err_avg = ["  > $path/Y_bp_err_avg.txt
echo "Y_gss_err_avg = ["  > $path/Y_gss_err_avg.txt

echo "Y_vc_std = ["  > $path/Y_vc_std.txt
echo "Y_bp_std = ["  > $path/Y_bp_std.txt
echo "Y_gss_std = ["  > $path/Y_gss_std.txt

echo "Y_vc_euclid = ["  > $path/Y_vc_euclid.txt
echo "Y_bp_euclid = ["  > $path/Y_bp_euclid.txt
echo "Y_gss_euclid = ["  > $path/Y_gss_euclid.txt

echo "Y_vc_edges = ["  > $path/Y_vc_edges.txt
echo "Y_bp_edges = ["  > $path/Y_bp_edges.txt
echo "Y_gss_edges = ["  > $path/Y_gss_edges.txt
echo "Y_exact_edges = ["  > $path/Y_exact_edges.txt



#Initialize the templ variables that keep track of the sum
point=1
while [ $point -le $number_point ]
do
    echo point:$point
    echo !!========== $point - point ==========!! >> $path/out.txt
    #4th  		6th		    7th			       8+9+10			11
    time_vc_tmp=0    err_avg_vc_tmp=0     err_stddev_vc_tmp=0     touched_edges_vc_tmp=0 	euclid_vc_tmp=0;
    time_bp_tmp=0    err_avg_bp_tmp=0     err_stddev_bp_tmp=0	touched_edges_bp_tmp=0 		euclid_bp_tmp=0;
    time_gss_tmp=0   err_avg_gss_tmp=0    err_stddev_gss_tmp=0    touched_edges_gss_tmp=0 	euclid_gss_tmp=0;
    time_exact_tmp=0 						touched_edges_exact_tmp=0 	
     

    samples=$(awk 'NR=='$(($point+1)) $path/X.txt)
    echo samples:$samples
    
    run=1
    while  [ $run -le $repetitions_4_each_point ]
    do 
	  echo run:$run
	  echo -------- $run - run -------- >> $path/out.txt 


	  python3 compare_exp.py 0.05 0.1 -s ${samples/\.*}  /data/people/matteo/centrsampl/$1 -u > temp.txt 
	  
          #Replace the  empty values with 0 (all but the last column!!)
	  sed -i 's/ ,/0 /g' temp.txt
	  sed -i 's/,/ /g' temp.txt

	  cat temp.txt >> $path/out.txt
         
          info_line=$(awk 'NR==2' temp.txt)
          stringarray=($info_line)          
          no_edges=${stringarray[2]}

	  #VC Assignment
	  vc_line=$(awk 'NR==4' temp.txt)
          stringarray=($vc_line)
	  time_vc_tmp=`echo $time_vc_tmp + ${stringarray[4]} | bc`
          err_avg_vc_tmp=$(echo | awk '{ print $1 + $2}' <<< ${stringarray[6]},$err_avg_vc_tmp )
          err_stddev_vc_tmp=$(echo | awk '{ print $1 + $2}' <<< ${stringarray[7]},$err_stddev_vc_tmp )
	  touched_edges_vc_tmp=`expr $touched_edges_vc_tmp + ${stringarray[8]/\.*} + ${stringarray[9]/\.*} + ${stringarray[10]/\.*}`
          euclid_vc_tmp=$(echo | awk '{ print $1 + $2}' <<< ${stringarray[11]},$euclid_vc_tmp )
	 # echo time:$time_vc_tmp err_avg:$err_avg_vc_tmp stdev:$err_stddev_vc_tmp edges:$touched_edges_vc_tmp

	  #BP Assignment
	  bp_line=$(awk 'NR==5' temp.txt)
	  stringarray=($bp_line)
	  time_bp_tmp=`echo $time_bp_tmp + ${stringarray[4]} | bc`
	  err_avg_bp_tmp=$(echo | awk '{ print $1 + $2}' <<< ${stringarray[6]},$err_avg_bp_tmp, )
          err_stddev_bp_tmp=$(echo | awk '{ print $1 + $2}' <<< ${stringarray[7]},$err_stddev_bp_tmp )
	  touched_edges_bp_tmp=`expr $touched_edges_bp_tmp + ${stringarray[8]/\.*} + ${stringarray[9]/\.*} + ${stringarray[10]/\.*}`
          euclid_bp_tmp=$(echo | awk '{ print $1 + $2}' <<< ${stringarray[11]},$euclid_bp_tmp )
	  #echo time:$time_bp_tmp err_avg:$err_avg_bp_tmp stdev:$err_stddev_bp_tmp edges:$touched_edges_bp_tmp

	  #GSS Assignment
	  gss_line=$(awk 'NR==6' temp.txt)
	  stringarray=($gss_line)
	  time_gss_tmp=`echo $time_gss_tmp + ${stringarray[4]} | bc`
	  err_avg_gss_tmp=$(echo | awk '{ print $1 + $2}' <<< ${stringarray[6]},$err_avg_gss_tmp, )
          err_stddev_gss_tmp=$(echo | awk '{ print $1 + $2}' <<< ${stringarray[7]},$err_stddev_gss_tmp )
	  touched_edges_gss_tmp=`expr $touched_edges_gss_tmp + ${stringarray[8]/\.*} + ${stringarray[9]/\.*} + ${stringarray[10]/\.*}`
          euclid_gss_tmp=$(echo | awk '{ print $1 + $2}' <<< ${stringarray[11]},$euclid_gss_tmp )
	  #echo time:$time_gss_tmp err_avg:$err_avg_gss_tmp stdev:$err_stddev_gss_tmp edges:$touched_edges_gss_tmp

	  #EXACT Assignment
	  exact_line=$(awk 'NR==7' temp.txt)
	  stringarray=($exact_line)
	  time_exact_tmp=`echo $time_exact_tmp + ${stringarray[4]} | bc`
	  touched_edges_exact_tmp=`expr $touched_edges_exact_tmp + ${stringarray[8]/\.*} + ${stringarray[9]/\.*} + ${stringarray[10]/\.*}`
	  #echo time:$time_exact_tmp err_avg:$err_avg_exact_tmp stdev:$err_stddev_exact_tmp edges:$touched_edges_exact_tmp
	
	  (( run += 1 ))
	  rm temp.txt

      done

      #Average the sum
     (bc <<< "scale=2; $time_vc_tmp/$repetitions_4_each_point") >> $path/Y_vc_time.txt
     (bc <<< "scale=2; $time_bp_tmp/$repetitions_4_each_point") >> $path/Y_bp_time.txt
     (bc <<< "scale=2; $time_gss_tmp/$repetitions_4_each_point") >> $path/Y_gss_time.txt
     (bc <<< "scale=2; $time_exact_tmp/$repetitions_4_each_point") >> $path/Y_exact_time.txt

      
      echo $err_avg_vc_tmp $repetitions_4_each_point | awk '{print $1 / $2}'   >> $path/Y_vc_err_avg.txt
      echo $err_avg_bp_tmp $repetitions_4_each_point | awk '{print $1 / $2}'   >> $path/Y_bp_err_avg.txt
      echo $err_avg_gss_tmp $repetitions_4_each_point | awk '{print $1 / $2}'   >> $path/Y_gss_err_avg.txt

      echo $err_stddev_vc_tmp $repetitions_4_each_point | awk '{print $1 / $2}'   >> $path/Y_vc_std.txt
      echo $err_stddev_bp_tmp $repetitions_4_each_point | awk '{print $1 / $2}'   >> $path/Y_bp_std.txt
      echo $err_stddev_gss_tmp $repetitions_4_each_point | awk '{print $1 / $2}'   >> $path/Y_gss_std.txt

      
      expr ${touched_edges_vc_tmp/\.*} / ${repetitions_4_each_point/\.*}   >> $path/Y_vc_edges.txt
      expr ${touched_edges_bp_tmp/\.*} / ${repetitions_4_each_point/\.*}   >> $path/Y_bp_edges.txt
      expr ${touched_edges_gss_tmp/\.*} / ${repetitions_4_each_point/\.*}   >> $path/Y_gss_edges.txt
      expr ${touched_edges_exact_tmp/\.*} / ${repetitions_4_each_point/\.*}   >> $path/Y_exact_edges.txt

      echo $euclid_vc_tmp $repetitions_4_each_point | awk '{print $1 / $2}'   >> $path/Y_vc_euclid.txt
      echo $euclid_bp_tmp $repetitions_4_each_point | awk '{print $1 / $2}'   >> $path/Y_bp_euclid.txt
      echo $euclid_gss_tmp $repetitions_4_each_point | awk '{print $1 / $2}'   >> $path/Y_gss_euclid.txt     

      (( point += 1 ))

done

echo "];"  >> $path/Y_vc_time.txt
echo "];"  >> $path/Y_bp_time.txt
echo "];"  >> $path/Y_gss_time.txt
echo "];"  >> $path/Y_exact_time.txt

echo "];"  >> $path/Y_vc_err_avg.txt
echo "];"  >> $path/Y_bp_err_avg.txt
echo "];"  >> $path/Y_gss_err_avg.txt

echo "];"  >> $path/Y_vc_std.txt
echo "];"  >> $path/Y_bp_std.txt
echo "];"  >> $path/Y_gss_std.txt

echo "];"  >> $path/Y_vc_edges.txt
echo "];"  >> $path/Y_bp_edges.txt
echo "];"  >> $path/Y_gss_edges.txt
echo "];"  >> $path/Y_exact_edges.txt

echo "];"  >> $path/Y_vc_euclid.txt
echo "];"  >> $path/Y_bp_euclid.txt
echo "];"  >> $path/Y_gss_euclid.txt


#Create the Matlab file

cat $path/X.txt >> $path/plots.m
cat $path/Y_vc_time.txt >> $path/plots.m
cat $path/Y_bp_time.txt >> $path/plots.m
cat $path/Y_gss_time.txt >> $path/plots.m
cat $path/Y_exact_time.txt >> $path/plots.m

echo "h1=figure; plot(X,Y_vc_time,'LineWidth',2); hold on; plot(X,Y_bp_time,'red','LineWidth',2);" >> $path/plots.m
echo "plot(X,Y_gss_time,'green','LineWidth',2); plot(X,Y_exact_time,'black','LineWidth',2);" >> $path/plots.m
echo "xlabel('Number of Samples'); ylabel('Time (in seconds)');"  >> $path/plots.m
echo "legend('VC-dim','BP','GSS','Exact')" >> $path/plots.m 
echo "grid on;" >> $path/plots.m
echo "title('$1, n=$no_nodes, m=$no_edges average of $repetitions_4_each_point runs');" >> $path/plots.m
echo "saveas(h1,'$path/time','jpg');" >> $path/plots.m


cat $path/Y_vc_err_avg.txt >> $path/plots.m
cat $path/Y_bp_err_avg.txt >> $path/plots.m
cat $path/Y_gss_err_avg.txt >> $path/plots.m

echo "h2=figure; plot(X,Y_vc_err_avg,'LineWidth',2); hold on; plot(X,Y_bp_err_avg,'red','LineWidth',2);" >> $path/plots.m
echo "plot(X,Y_gss_err_avg,'green','LineWidth',2);" >> $path/plots.m
echo "xlabel('Number of Samples'); ylabel('Average Absolute Deviation');"  >> $path/plots.m
echo "legend('VC-dim','BP','GSS')" >> $path/plots.m 
echo "grid on;" >> $path/plots.m
echo "title('$1, n=$no_nodes, m=$no_edges average of $repetitions_4_each_point runs');" >> $path/plots.m
echo "saveas(h2,'$path/err_avg','jpg');" >> $path/plots.m



cat $path/Y_vc_edges.txt >> $path/plots.m
cat $path/Y_bp_edges.txt >> $path/plots.m
cat $path/Y_gss_edges.txt >> $path/plots.m
cat $path/Y_exact_edges.txt >> $path/plots.m

echo "h3=figure; plot(X,Y_vc_edges,'LineWidth',2); hold on; plot(X,Y_bp_edges,'red','LineWidth',2);" >> $path/plots.m
echo "plot(X,Y_gss_edges,'green','LineWidth',2); plot(X,Y_exact_edges,'black','LineWidth',2);" >> $path/plots.m
echo "xlabel('Number of Samples'); ylabel('Traversed Edges');"  >> $path/plots.m
echo "legend('VC-dim','BP','GSS','Exact')" >> $path/plots.m 
echo "grid on;" >> $path/plots.m
echo "title('$1, n=$no_nodes, m=$no_edges average of $repetitions_4_each_point runs');" >> $path/plots.m
echo "saveas(h3,'$path/edges','jpg');" >> $path/plots.m


cat $path/Y_vc_euclid.txt >> $path/plots.m
cat $path/Y_bp_euclid.txt >> $path/plots.m
cat $path/Y_gss_euclid.txt >> $path/plots.m

echo "h4=figure; plot(X,Y_vc_euclid,'LineWidth',2); hold on; plot(X,Y_bp_euclid,'red','LineWidth',2);" >> $path/plots.m
echo "plot(X,Y_gss_euclid,'green','LineWidth',2);" >> $path/plots.m
echo "xlabel('Number of Samples'); ylabel('Euclidean Distance');"  >> $path/plots.m
echo "legend('VC-dim','BP','GSS')" >> $path/plots.m 
echo "grid on;" >> $path/plots.m
echo "title('$1, n=$no_nodes, m=$no_edges average of $repetitions_4_each_point runs');" >> $path/plots.m
echo "saveas(h4,'$path/euclid','jpg');" >> $path/plots.m



