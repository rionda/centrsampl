#!
#
# $1 should be the graph dataset for the experiment
# $2 points
# $3 number_runs
#  X-axis: samples
# We create a out.txt that keeps track of all the data
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

#Create a new directory, use the pid in order to avoid  overwriting a useful run

path=$1

cat $path/epsilon.txt > $path/X.txt


#Initialize the files
echo "Y_vc_time = ["  > $path/Y_vc_time.txt
echo "Y_bp_time = ["  > $path/Y_bp_time.txt
echo "Y_exact_time = ["  > $path/Y_exact_time.txt


#Initialize the templ variables that keep track of the sum
point=1
while [ $point -lt `expr $2 + 1` ]
do
     

     (python3 get_results.py $path/out_files/out_vc_$point.picklez time_avg) >> $path/Y_vc_time.txt
     (python3 get_results.py $path/out_files/out_bp_$point.picklez time_avg) >> $path/Y_bp_time.txt
    # (python3 get_results.py $path/out_files/out_gss_$point.picklez time_avg) >> $path/Y_gss_time.txt
      (( point += 1 ))

done

(python3 get_results.py $path/out_files/out_exact_1.picklez time_avg) >> $path/Y_exact_time.txt 

echo "];"  >> $path/Y_vc_time.txt
echo "];"  >> $path/Y_bp_time.txt
#echo "];"  >> $path/Y_gss_time.txt
echo "];"  >> $path/Y_exact_time.txt
                                                                                                        


#Create the Matlab file

cat $path/epsilon.txt >> $path/plot_epsilon_time.m
cat $path/Y_vc_time.txt >> $path/plot_epsilon_time.m
cat $path/Y_bp_time.txt >> $path/plot_epsilon_time.m
#cat $path/Y_gss_time.txt >> $path/plot_epsilon_time.m
cat $path/Y_exact_time.txt >> $path/plot_epsilon_time.m


echo "Y_exact_time = repmat(Y_exact_time,size(Y_vc_time,1),1);" >> $path/plot_epsilon_time.m
echo "h1=figure; plot(epsilon,Y_vc_time,'LineWidth',2);hold on; plot(epsilon,Y_bp_time,'r--','LineWidth',2);" >> $path/plot_epsilon_time.m
echo "plot(epsilon,Y_exact_time,'k-.','LineWidth',2);" >> $path/plot_epsilon_time.m
echo "plot(epsilon,Y_vc_time,'O','LineWidth',3);plot(epsilon,Y_bp_time,'rO','LineWidth',3);plot(epsilon,Y_exact_time,'kO','LineWidth',3);" >> $path/plot_epsilon_time.m
echo "xlabel('epsilon'); ylabel('Running Time (seconds)');"  >> $path/plot_epsilon_time.m
echo "legend('VC-dim','BP','Exact')" >> $path/plot_epsilon_time.m 
echo "grid on;" >> $path/plot_epsilon_time.m
echo "title('$path , |V|= , |E|= , \delta= 0.1 ,runs= $3');" >> $path/plot_epsilon_time.m
echo "figureHandle = gcf;set(findall(figureHandle,'type','text'),'fontSize',12,'fontWeight','bold')" >> $path/plot_epsilon_time.m 


rm $path/X.txt
rm $path/Y_vc_time.txt
rm $path/Y_bp_time.txt
#rm $path/Y_gss_time.txt
rm $path/Y_exact_time.txt
