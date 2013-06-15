#!
#
# $1 should be the graph dataset for the experiment
# $2 should be either -u or -dir
# $3 if it is -d then we are considering the exact value of the diameter which is passed over $4
# $4 contains the value of the diameter in case we have -d as an argument at $3
# Y-axis: time, err_avg, touched_edges
#  X-axis: samples
#

# Check whether the file exists
#if ! [ -f $1 ]
#then 
#  echo -e "\n File $1, is not at directory "
#fi

dataset_tmp=${1//// }
str=($dataset_tmp)
dataset=${str[${#str[*]}-1]}
dataset=${dataset/\.*}

echo $dataset


#Create a new directory, use the pid in order to avoid  overwriting a useful run
mkdir ./${dataset}_epsilon_$$
path=./${dataset}_epsilon_$$

mkdir ./${dataset}_epsilon_$$/out_files
path_out=./${dataset}_epsilon_$$/out_files


#Compute the different sample sizes

epsilon_val="0.005 0.01 0.015 0.02 0.04 0.06 0.08 0.1"
#percentages_val="0.01 0.05"
epsilon=($epsilon_val)
number_point=${#epsilon[@]}

echo "epsilon = [" >> $path/epsilon.txt


#Initialize the X-axis (number of samples)
iter=0
while [ $iter -lt $number_point ]
do
  echo "${epsilon[$iter]}" >> $path/epsilon.txt
  (( iter += 1 ))
done
echo "];"  >> $path/epsilon.txt

# Each run for a fixed sample size is repeated $repetitions and averaged.
repetitions_4_each_point=5


point=1
while [ $point -lt `expr $number_point + 1` ]
do
    echo point:$point
    echo !!========== $point - point ==========!! 


    curr_epsilon=$(awk 'NR=='$(($point+1)) $path/epsilon.txt)
    echo epsilon:$curr_epsilon


    if [ $3 == '-d' ] 
    then
        echo "diameter given as an input"
        #Only works for undirected
        python3 vc_sample_experiment.py $curr_epsilon 0.1 $repetitions_4_each_point $1  $path_out/out_vc_$point.picklez $2 -d $4
    else
        python3 vc_sample_experiment.py $curr_epsilon 0.1 $repetitions_4_each_point $1  $path_out/out_vc_$point.picklez $2
    fi      

    python3 bp_sample_experiment.py $curr_epsilon 0.1 $repetitions_4_each_point $1  $path_out/out_bp_$point.picklez  $2
    #python3 gss_sample_experiment.py $curr_epsilon 0.1 $repetitions_4_each_point $1  $path_out/out_gss_$point.picklez $2
    ((point += 1 ))

done

python3 exact_experiment.py 5 $1 $path_out/out_exact_1.picklez $2
