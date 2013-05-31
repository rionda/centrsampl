#!
#
# $1 should be the graph dataset for the experiment
# $2 points
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

cat $path/Sample_size.txt > $path/X.txt


#Initialize the files
echo "Y_vc_euclid = ["  > $path/Y_vc_euclid.txt
echo "Y_bp_euclid = ["  > $path/Y_bp_euclid.txt
echo "Y_gss_euclid = ["  > $path/Y_gss_euclid.txt




#Initialize the templ variables that keep track of the sum
point=1
while [ $point -le $2 ]
do
     

     (python3 comparison_exact.py vc $path $point $2 euclid_dist) >> $path/Y_vc_euclid.txt
     (python3 comparison_exact.py bp $path $point $2 euclid_dist) >> $path/Y_bp_euclid.txt
     (python3 comparison_exact.py gss $path $point $2 euclid_dist) >> $path/Y_gss_euclid.txt
  
      (( point += 1 ))

done

echo "];"  >> $path/Y_vc_euclid.txt
echo "];"  >> $path/Y_bp_euclid.txt
echo "];"  >> $path/Y_gss_euclid.txt

#Create the Matlab file

cat $path/Sample_size.txt >> $path/plot_euclid.m
cat $path/Y_vc_euclid.txt >> $path/plot_euclid.m
cat $path/Y_bp_euclid.txt >> $path/plot_euclid.m
cat $path/Y_gss_euclid.txt >> $path/plot_euclid.m

echo "h1=figure; plot(Sample_size,Y_vc_euclid,'LineWidth',2); hold on; plot(Sample_size,Y_bp_euclid,'red','LineWidth',2);" >> $path/plot_euclid.m
echo "plot(Sample_size,Y_gss_euclid,'green','LineWidth',2);" >> $path/plot_euclid.m
echo "xlabel('Number of Samples'); ylabel('Euclidean Distance');"  >> $path/plot_euclid.m
echo "legend('VC-dim','BP','GSS')" >> $path/plot_euclid.m 
echo "grid on;" >> $path/plot_euclid.m
echo "title('$1, average of $2 runs');" >> $path/plot_euclid.m
echo "saveas(h1,'$path/euclid','jpg');" >> $path/plot_euclid.m

rm $path/X.txt
rm $path/Y_vc_euclid.txt
rm $path/Y_bp_euclid.txt
rm $path/Y_gss_euclid.txt
