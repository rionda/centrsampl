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
%345.66080991
76.3875432144
34.0757890386
19.1192618328
4.8656827410000005
2.1844766172
1.2294223374
0.8328052676000001
];
Y_bp_time = [
%1300.8116227927999
255.0304381896
113.28290398300001
63.7975101012
15.9706189806
7.164007571799999
3.9707087725999997
2.5566581002
];
Y_exact_time = [
49.4463277805
];
Y_exact_time = repmat(Y_exact_time,size(Y_vc_time,1),1);
h1=figure; plot(epsilon,Y_vc_time,'LineWidth',2);hold on; plot(epsilon,Y_bp_time,'r--','LineWidth',2);
plot(epsilon,Y_exact_time,'k','LineWidth',2);
plot(epsilon,Y_vc_time,'O','LineWidth',3);plot(epsilon,Y_bp_time,'rd','LineWidth',3);%plot(epsilon,Y_exact_time,'kO','LineWidth',3);
xlabel('epsilon'); ylabel('Running Time (seconds)');
legend('VC (diam-2approx)','BP','Exact')
grid on;
title('ca-HepPh-u , |V|=12.008 , |E|=237.010 , \delta= 0.1 ,runs= 5');
figureHandle = gcf;set(findall(figureHandle,'type','text'),'fontSize',12,'fontWeight','bold')
set(gca,'yscale','log')
xlim([.005 .105])
ylim([.5 500])
