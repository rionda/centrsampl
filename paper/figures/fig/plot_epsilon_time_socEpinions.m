epsilon = [
%0.005
0.01
0.015
0.02
0.04
0.06
0.08
0.1
];
Y_vc_time = [
%1088.7378170186
272.4693203664
121.03797315659999
67.88883341980002
17.066340181999998
7.7217557844
4.328977859
2.8328853350000003
];
Y_vc_time_UB = [
%3343.9594992282
838.2111340399999
372.3026519856
210.163312061
52.81351733
23.830138506399997
13.5420870788
8.668846674
];
Y_bp_time = [
%3600.0
1156.567412923
514.4032657437999
288.785766808
72.65281344159999
32.485941883
18.3526729154
11.913467579
];
Y_exact_time = [
1231.6448763946667
];
Y_exact_time = repmat(Y_exact_time,size(Y_vc_time,1),1);

h1=figure; plot(epsilon,Y_vc_time,'LineWidth',2);hold on;plot(epsilon,Y_vc_time_UB,'g-.','LineWidth',2); plot(epsilon,Y_bp_time,'r--','LineWidth',2);
plot(epsilon,Y_exact_time,'k','LineWidth',2);
plot(epsilon,Y_vc_time,'O','LineWidth',2,'MarkerSize',8);plot(epsilon,Y_vc_time_UB,'gs','LineWidth',2,'MarkerSize',8);
plot(epsilon,Y_bp_time,'rd','LineWidth',2,'MarkerSize',8);%plot(epsilon,Y_exact_time,'k*','LineWidth',2,'MarkerSize',8);
xlabel('epsilon'); ylabel('Running Time (seconds)');
legend('VC (diam-exact)','VC (diam-UB)','BP','Exact')
grid on;
title('soc-Epinions1-d , |V|=75,879 , |E|=508,837 , \delta= 0.1 , runs= 5');
figureHandle = gcf;set(findall(figureHandle,'type','text'),'fontSize',12,'fontWeight','bold')
set(gca,'YScale','log');
xlim([.005 .105])

