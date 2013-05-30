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
echo "Y_vc_edges = ["  > $path/Y_vc_edges.txt
echo "Y_bp_edges = ["  > $path/Y_bp_edges.txt
echo "Y_gss_edges = ["  > $path/Y_gss_edges.txt
echo "Y_exact_edges = ["  > $path/Y_exact_edges.txt




#Initialize the templ variables that keep track of the sum
point=1
while [ $point -le $2 ]
do
    
     fwd=$(python3 get_results.py $path/out_files/out_vc_$point.picklez forward_touched_edges_avg)
     bwd=$(python3 get_results.py $path/out_files/out_vc_$point.picklez backward_touched_edges_avg)
     (echo $fwd $bwd | awk '{print $1 + $2}')  >> $path/Y_vc_edges.txt

     fwd=$(python3 get_results.py $path/out_files/out_bp_$point.picklez forward_touched_edges_avg)
     bwd=$(python3 get_results.py $path/out_files/out_bp_$point.picklez backward_touched_edges_avg)
     (echo $fwd $bwd | awk '{print $1 + $2}')  >> $path/Y_bp_edges.txt
     

     fwd=$(python3 get_results.py $path/out_files/out_gss_$point.picklez forward_touched_edges_avg)
     bwd=$(python3 get_results.py $path/out_files/out_gss_$point.picklez backward_touched_edges_avg)
     (echo $fwd $bwd | awk '{print $1 + $2}')  >> $path/Y_gss_edges.txt


     fwd=$(python3 get_results.py $path/out_files/out_exact_$point.picklez forward_touched_edges)
     bwd=$(python3 get_results.py $path/out_files/out_exact_$point.picklez backward_touched_edges)
     (echo $fwd $bwd | awk '{print $1 + $2}')  >> $path/Y_exact_edges.txt

      (( point += 1 ))

done

echo "];"  >> $path/Y_vc_edges.txt
echo "];"  >> $path/Y_bp_edges.txt
echo "];"  >> $path/Y_gss_edges.txt
echo "];"  >> $path/Y_exact_edges.txt



#Create the Matlab file

cat $path/Sample_size.txt >> $path/plot_edges.m
cat $path/Y_vc_edges.txt >> $path/plot_edges.m
cat $path/Y_bp_edges.txt >> $path/plot_edges.m
cat $path/Y_gss_edges.txt >> $path/plot_edges.m
cat $path/Y_exact_edges.txt >> $path/plot_edges.m

echo "h1=figure; plot(Sample_size,Y_vc_edges,'LineWidth',2); hold on; plot(Sample_size,Y_bp_edges,'red','LineWidth',2);" >> $path/plot_edges.m
echo "plot(Sample_size,Y_gss_edges,'green','LineWidth',2); plot(Sample_size,Y_exact_edges,'black','LineWidth',2);" >> $path/plot_edges.m
echo "xlabel('Number of Samples'); ylabel('Edges Traversed');"  >> $path/plot_edges.m
echo "legend('VC-dim','BP','GSS','Exact')" >> $path/plot_edges.m 
echo "grid on;" >> $path/plot_edges.m
echo "title('$1, average of $2 runs');" >> $path/plot_edges.m
echo "saveas(h1,'$path/edges','jpg');" >> $path/plot_edges.m

rm $path/X.txt
rm $path/Y_vc_edges.txt
rm $path/Y_bp_edges.txt
rm $path/Y_gss_edges.txt
rm $path/Y_exact_edges.txt
