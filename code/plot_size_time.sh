#!
#
# $1 should be the graph dataset for the experiment
# $2 points
#  X-axis: samples
# We create a out.txt that keeps track of all the data
#

# Check whether the file exists
if ! [ -f $1 ]
then 
  echo -e "\n File $1, is not at directory "
fi

dataset_tmp=${1//// }
str=($dataset_tmp)
dataset=${str[${#str[*]}-1]}
dataset=${dataset/\.*}

#Create a new directory, use the pid in order to avoid  overwriting a useful run

path=$1

cat $path/Sample_size.txt > $path/X.txt


#Initialize the files
echo "Y_vc_time = ["  > $path/Y_vc_time.txt
echo "Y_bp_time = ["  > $path/Y_bp_time.txt
echo "Y_gss_time = ["  > $path/Y_gss_time.txt
echo "Y_exact_time = ["  > $path/Y_exact_time.txt




#Initialize the templ variables that keep track of the sum
point=1
while [ $point -le $2 ]
do
     

     (python3 get_results.py $path/out_files/out_vc_$point.picklez time_avg) >> $path/Y_vc_time.txt
     (python3 get_results.py $path/out_files/out_bp_$point.picklez time_avg) >> $path/Y_bp_time.txt
     (python3 get_results.py $path/out_files/out_gss_$point.picklez time_avg) >> $path/Y_gss_time.txt
     (python3 get_results.py $path/out_files/out_exact_$point.picklez time_avg) >> $path/Y_exact_time.txt 

      (( point += 1 ))

done

echo "];"  >> $path/Y_vc_time.txt
echo "];"  >> $path/Y_bp_time.txt
echo "];"  >> $path/Y_gss_time.txt
echo "];"  >> $path/Y_exact_time.txt



#Create the Matlab file

cat $path/Sample_size.txt >> $path/plot_time.m
cat $path/Y_vc_time.txt >> $path/plot_time.m
cat $path/Y_bp_time.txt >> $path/plot_time.m
cat $path/Y_gss_time.txt >> $path/plot_time.m
cat $path/Y_exact_time.txt >> $path/plot_time.m

echo "h1=figure; plot(Sample_size,Y_vc_time,'LineWidth',2); hold on; plot(Sample_size,Y_bp_time,'red','LineWidth',2);" >> $path/plot_time.m
echo "plot(Sample_size,Y_gss_time,'green','LineWidth',2); plot(Sample_size,Y_exact_time,'black','LineWidth',2);" >> $path/plot_time.m
echo "xlabel('Number of Samples'); ylabel('Time (in seconds)');"  >> $path/plot_time.m
echo "legend('VC-dim','BP','GSS','Exact')" >> $path/plot_time.m 
echo "grid on;" >> $path/plot_time.m
echo "title('$1, average of $2 runs');" >> $path/plot_time.m
echo "saveas(h1,'$path/time','jpg');" >> $path/plot_time.m

rm $path/X.txt
rm $path/Y_vc_time.txt
rm $path/Y_bp_time.txt
rm $path/Y_gss_time.txt
rm $path/Y_exact_time.txt
