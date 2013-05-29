#!
#
# $1 should be the graph dataset for the experiment
# $2 should be either -u or -d
# Y-axis: time, err_avg, touched_edges
#  X-axis: samples
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
mkdir ./${dataset}_fixedSample_$$
path=./${dataset}_fixedSample_$$

mkdir ./${dataset}_fixedSample_$$/out_files
path_out=./${dataset}_fixedSample_$$/out_files


no_nodes=$(python3 number_nodes.py $1)
#no_nodes=196591

#Compute the different sample sizes

percentages_val="0.01 0.05 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45"
#percentages_val="0.01 0.05 0.1"
percentages=($percentages_val)
number_point=${#percentages[@]}

#Initialize the X-axis (number of samples)
echo "Sample_size = ["  > $path/Sample_size.txt
iter=0
while [ $iter -lt $number_point ]
do
  echo "${percentages[$iter]} * $no_nodes" | bc -l >> $path/Sample_size.txt
  (( iter += 1 ))
done
echo "];"  >> $path/Sample_size.txt


# Each run for a fixed sample size is repeated $repetitions and averaged.
repetitions_4_each_point=20


point=1
while [ $point -lt $number_point ]
do
    echo point:$point
    echo !!========== $point - point ==========!! 


    samples=$(awk 'NR=='$(($point+1)) $path/Sample_size.txt)
    echo samples:$samples
    


    #Only works for undirected
    python3 vc_sample_experiment.py 0.05 0.1 $repetitions_4_each_point $1 $path_out/out_vc_$point.picklez -u -s ${samples/\.*}
    python3 bp_sample_experiment.py 0.05 0.1 $repetitions_4_each_point $1 $path_out/out_bp_$point.picklez -u -s ${samples/\.*}
    python3 gss_sample_experiment.py 0.05 0.1 $repetitions_4_each_point $1 $path_out/out_gss_$point.picklez -u -s ${samples/\.*}
    #We only run exact two times because the variance is really small from run to run
    python3 exact_experiment.py 2 $1 $path_out/out_exact_$point.picklez -u   

    (( point += 1 ))

done
