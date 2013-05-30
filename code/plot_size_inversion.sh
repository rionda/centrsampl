#!
#
# $1 should be the graph dataset for the experiment
# $2 points
#  X-axis: samples
# We create a out.txt that keeps track of all the data
#
# TOO SLOW!!
# Check whether the file exists



dataset_tmp=${1//// }
str=($dataset_tmp)
dataset=${str[${#str[*]}-1]}
dataset=${dataset/\.*}

#Create a new directory, use the pid in order to avoid  overwriting a useful run

path=$1

cat $path/Sample_size.txt > $path/X.txt


#Initialize the files
echo "Y_vc_inv = ["  > $path/Y_vc_inv.txt
echo "Y_bp_inv = ["  > $path/Y_bp_inv.txt
echo "Y_gss_inv = ["  > $path/Y_gss_inv.txt




#Initialize the templ variables that keep track of the sum
point=1
while [ $point -le $2 ]
do
     
      echo point: $point
     (python3 comparison_exact.py vc $path $point $2 inversions) >> $path/Y_vc_inv.txt
     (python3 comparison_exact.py bp $path $point $2 inversions) >> $path/Y_bp_inv.txt
     (python3 comparison_exact.py gss $path $point $2 inversions) >> $path/Y_gss_inv.txt
  
      (( point += 1 ))

done

echo "];"  >> $path/Y_vc_inv.txt
echo "];"  >> $path/Y_bp_inv.txt
echo "];"  >> $path/Y_gss_inv.txt

#Create the Matlab file

cat $path/Sample_size.txt >> $path/plot_inv.m
cat $path/Y_vc_inv.txt >> $path/plot_inv.m
cat $path/Y_bp_inv.txt >> $path/plot_inv.m
cat $path/Y_gss_inv.txt >> $path/plot_inv.m

echo "h1=figure; plot(Sample_size,Y_vc_inv,'LineWidth',2); hold on; plot(Sample_size,Y_bp_inv,'red','LineWidth',2);" >> $path/plot_inv.m
echo "plot(Sample_size,Y_gss_inv,'green','LineWidth',2);" >> $path/plot_inv.m
echo "xlabel('Number of Samples'); ylabel('Inversion Distance');"  >> $path/plot_inv.m
echo "legend('VC-dim','BP','GSS')" >> $path/plot_inv.m 
echo "grid on;" >> $path/plot_inv.m
echo "title('$1, average of $2 runs');" >> $path/plot_inv.m
echo "saveas(h1,'$path/inv','jpg');" >> $path/plot_inv.m

rm $path/X.txt
rm $path/Y_vc_inv.txt
rm $path/Y_bp_inv.txt
rm $path/Y_gss_inv.txt
