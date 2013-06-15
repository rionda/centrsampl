#!
#
# $1 should be the graph dataset for the experiment
# $2 points
# $3 number_runs
#  X-axis: samples
# We create a out.txt that keeps track of all the data
#



dataset_tmp=${1//// }
str=($dataset_tmp)
dataset=${str[${#str[*]}-1]}
dataset=${dataset/\.*}

#Create a new directory, use the pid in order to avoid  overwriting a useful run

path=$1

cat $path/epsilon.txt > $path/X.txt


#Initialize the files
echo "Y_vc_edges = ["  > $path/Y_vc_edges.txt
echo "Y_bp_edges = ["  > $path/Y_bp_edges.txt
# echo "Y_gss_edges = ["  > $path/Y_gss_edges.txt
echo "Y_exact_edges = ["  > $path/Y_exact_edges.txt




#Initialize the templ variables that keep track of the sum
point=1
while [ $point -lt `expr $2 + 1` ]
do
    
     fwd=$(python3 get_results.py $path/out_files/out_vc_$point.picklez forward_touched_edges_avg)
     bwd=$(python3 get_results.py $path/out_files/out_vc_$point.picklez backward_touched_edges_avg)
     (echo $fwd $bwd | awk '{print $1 + $2}')  >> $path/Y_vc_edges.txt

     fwd=$(python3 get_results.py $path/out_files/out_bp_$point.picklez forward_touched_edges_avg)
     bwd=$(python3 get_results.py $path/out_files/out_bp_$point.picklez backward_touched_edges_avg)
     (echo $fwd $bwd | awk '{print $1 + $2}')  >> $path/Y_bp_edges.txt
     

 #    fwd=$(python3 get_results.py $path/out_files/out_gss_$point.picklez forward_touched_edges_avg)
 #    bwd=$(python3 get_results.py $path/out_files/out_gss_$point.picklez backward_touched_edges_avg)
 #    (echo $fwd $bwd | awk '{print $1 + $2}')  >> $path/Y_gss_edges.txt

      (( point += 1 ))

done

fwd=$(python3 get_results.py $path/out_files/out_exact_1.picklez forward_touched_edges)
bwd=$(python3 get_results.py $path/out_files/out_exact_1.picklez backward_touched_edges)
(echo $fwd $bwd | awk '{print $1 + $2}')  >> $path/Y_exact_edges.txt


echo "];"  >> $path/Y_vc_edges.txt
echo "];"  >> $path/Y_bp_edges.txt
# echo "];"  >> $path/Y_gss_edges.txt
echo "];"  >> $path/Y_exact_edges.txt



#Create the Matlab file

cat $path/epsilon.txt >> $path/plot_epsilon_edges.m
cat $path/Y_vc_edges.txt >> $path/plot_epsilon_edges.m
cat $path/Y_bp_edges.txt >> $path/plot_epsilon_edges.m
cat $path/Y_exact_edges.txt >> $path/plot_epsilon_edges.m


echo "Y_exact_edges = repmat(Y_exact_edges,size(Y_vc_edges,1),1);" >> $path/plot_epsilon_edges.m
echo "h1=figure; plot(epsilon,Y_vc_edges,'LineWidth',2); hold on; plot(epsilon,Y_bp_edges,'r--','LineWidth',2);" >> $path/plot_epsilon_edges.m
echo "plot(epsilon,Y_exact_edges,'k-.','LineWidth',2);" >> $path/plot_epsilon_edges.m
echo "plot(epsilon,Y_vc_edges,'O','LineWidth',3);plot(epsilon,Y_bp_edges,'rO','LineWidth',3);plot(epsilon,Y_exact_edges,'kO','LineWidth',3);" >> $path/plot_epsilon_edges.m 
echo "xlabel('epsilon'); ylabel('Average # of touched edges');"  >> $path/plot_epsilon_edges.m
echo "legend('VC-dim','BP','Exact')" >> $path/plot_epsilon_edges.m 
echo "grid on;" >> $path/plot_epsilon_edges.m
echo "title('$path , |V|= , |E|= , \delta= 0.1 ,runs= $3');" >> $path/plot_epsilon_edges.m
echo "figureHandle = gcf;set(findall(figureHandle,'type','text'),'fontSize',12,'fontWeight','bold')" >> $path/plot_epsilon_edges.m 


rm $path/X.txt
rm $path/Y_vc_edges.txt
rm $path/Y_bp_edges.txt
rm $path/Y_exact_edges.txt
