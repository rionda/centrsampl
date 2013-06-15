#!
#
# $1 should be the graph dataset for the experiment
# $2 points
# $3 number_runs
#  X-axis: samples
# We create a out.txt that keeps track of all the data
#

# Check whether the file exists



dataset_tmp=${1//// }
str=($dataset_tmp)
dataset=${str[${#str[*]}-1]}
dataset=${dataset/\.*}

#Create a new directory, use the pid in order to avoid  overwriting a useful run

path=$1


echo "epsilon_samples = {" >> $path/epsilon_samples.txt 


#Initialize the templ variables that keep track of the sum
point=1
while [ $point -lt `expr $2 + 1` ]
do
 
     echo "Y_$point = [" > $path/Y_$point.txt
    
     (python3 error_statistics_vc.py $path $point $3) >> $path/Y_$point.txt
     echo "];" >> $path/Y_$point.txt
 
     temp_sample=`python3 get_results.py $path/out_files/out_vc_$point.picklez sample_size`
     temp_line=`expr $point + 1` 
     temp_epsilon=`awk "NR==$temp_line" $path/epsilon.txt`
     
    echo "'$temp_epsilon(${temp_sample/.*})'" >> $path/epsilon_samples.txt

     cat $path/Y_$point.txt >> $path/plot_error.m
     echo "plot($point,Y_$point(1),'x','Linewidth',2);hold on;plot($point,Y_$point(2),'V','Linewidth',2);hold on;plot($point,Y_$point(3),'O','Linewidth',2);" >> $path/plot_error.m
     rm $path/Y_$point.txt
     (( point += 1 ))
done

echo "};" >> $path/epsilon_samples.txt 


#Create the Matlab file

cat $path/epsilon_samples.txt >> $path/plot_error.m
echo "legend('Average','Standard Deviation','Maximum Value')" >> $path/plot_error.m 
echo "set(gca, 'YScale', 'log'); xlabel('epsilon (sample size)'); " >> $path/plot_error.m
echo "ylabel('Absolute difference (log-scale)');title('$path , |V|= , |E|= , \delta= 0.1 ,runs= $3');" >> $path/plot_error.m
echo "epsilon_samples=[0; epsilon_samples; 0.15]" >> $path/plot_error.m
echo "set(gca,'XTickLabel',epsilon_samples);set(gca,'XGrid','off','YGrid','on','ZGrid','off');" >> $path/plot_error.m
echo "xlim([0 `expr $2 + 1`]);" >> $path/plot_error.m
echo "figureHandle = gcf;set(findall(figureHandle,'type','text'),'fontSize',12,'fontWeight','bold')" >> $path/plot_error.m 
