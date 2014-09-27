%Y_1 = [
%8.8673961195938e-06
%2.9734977997871873e-05
%0.0005409331274614793
%];
%plot(1,Y_1(1),'x','Linewidth',2);hold on;plot(1,Y_1(2),'V','Linewidth',2);hold on;plot(1,Y_1(3),'O','Linewidth',2);
Y_2 = [
3.0632436342378774e-05
0.00010320019578623422
0.0014772171610517477
];

Y_2_UB = [
1.7530290064575606e-05
5.8241795183129094e-05
0.000702729249995029
];
plot(2,Y_2(1),'s','Linewidth',2);hold on;plot(2,Y_2(2),'V','Linewidth',2);hold on;plot(2,Y_2(3),'O','Linewidth',2);

plot(2,Y_2_UB(1),'rd','Linewidth',2);hold on;plot(2,Y_2_UB(2),'r^','Linewidth',2);hold on;plot(2,Y_2_UB(3),'r<','Linewidth',2);

Y_3 = [
4.45120356145359e-05
0.00015375253409034034
0.002107407436022196
];
plot(3,Y_3(1),'s','Linewidth',2);hold on;plot(3,Y_3(2),'V','Linewidth',2);hold on;plot(3,Y_3(3),'O','Linewidth',2);
Y_4 = [
5.6689411917162284e-05
0.00020700921272607023
0.002289601651946768
];
plot(4,Y_4(1),'s','Linewidth',2);hold on;plot(4,Y_4(2),'V','Linewidth',2);hold on;plot(4,Y_4(3),'O','Linewidth',2);

Y_5 = [
9.177136448611925e-05
0.0004235828665704358
0.0058639357145690504
];
plot(5,Y_5(1),'s','Linewidth',2);hold on;plot(5,Y_5(2),'V','Linewidth',2);hold on;plot(5,Y_5(3),'O','Linewidth',2);

Y_6 = [
0.00011418146298969938
0.0006453911106164502
0.007255110954828517
];
plot(6,Y_6(1),'s','Linewidth',2);hold on;plot(6,Y_6(2),'V','Linewidth',2);hold on;plot(6,Y_6(3),'O','Linewidth',2);

Y_7 = [
0.00012581927430193855
0.0008388790208168911
0.010407752190923287
];
plot(7,Y_7(1),'s','Linewidth',2);hold on;plot(7,Y_7(2),'V','Linewidth',2);hold on;plot(7,Y_7(3),'O','Linewidth',2);

Y_8 = [
0.00014109786683816827
0.0010908783915849008
0.014547994058076084
];
plot(8,Y_8(1),'s','Linewidth',2);hold on;plot(8,Y_8(2),'V','Linewidth',2);hold on;plot(8,Y_8(3),'O','Linewidth',2);
epsilon_samples = {
%'0.005(386052)'
'0.01(96513)'
'0.015(42895)'
'0.02(24129)'
'0.04(6033)'
'0.06(2681)'
'0.08(1509)'
'0.1(966)'
};

Y_3_UB = [
2.6558927025777975e-05
9.080305098170421e-05
0.0013529423527893457
];
plot(3,Y_3_UB(1),'rd','Linewidth',2);hold on;plot(3,Y_3_UB(2),'r^','Linewidth',2);hold on;plot(3,Y_3_UB(3),'r<','Linewidth',2);

Y_4_UB = [
3.477564540165907e-05
0.0001169983114699522
0.0017342943742366026
];
plot(4,Y_4_UB(1),'rd','Linewidth',2);hold on;plot(4,Y_4_UB(2),'r^','Linewidth',2);hold on;plot(4,Y_4_UB(3),'r<','Linewidth',2);
Y_5_UB = [
6.275424247218937e-05
0.00023679414996934242
0.0032740928444656052
];
plot(5,Y_5_UB(1),'rd','Linewidth',2);hold on;plot(5,Y_5_UB(2),'r^','Linewidth',2);hold on;plot(5,Y_5_UB(3),'r<','Linewidth',2);
Y_6_UB = [
8.371306427430313e-05
0.00036179442396893177
0.004975878604920525
];
plot(6,Y_6_UB(1),'rd','Linewidth',2);hold on;plot(6,Y_6_UB(2),'r^','Linewidth',2);hold on;plot(6,Y_6_UB(3),'r<','Linewidth',2);
Y_7_UB = [
9.952251665763941e-05
0.0004932945861748279
0.007046973712976139
];
plot(7,Y_7_UB(1),'rd','Linewidth',2);hold on;plot(7,Y_7_UB(2),'r^','Linewidth',2);hold on;plot(7,Y_7_UB(3),'r<','Linewidth',2);
Y_8_UB = [
0.00011208788119278083
0.00062769939235782
0.011170841548663131
];
plot(8,Y_8_UB(1),'rd','Linewidth',2);hold on;plot(8,Y_8_UB(2),'r^','Linewidth',2);hold on;plot(8,Y_8_UB(3),'r<','Linewidth',2);


legend('Avg (diam-exact)','Avg+Stddev (diam-exact)','Max (diam-exact)','Avg (diam-UB)','Avg+Stddev (diam-UB)','Max (diam-UB)')
set(gca, 'YScale', 'log'); xlabel('epsilon (sample size)'); 
ylabel('Absolute estimation error ');title('soc-Epinions1-d , |V|=75,879 , |E|=508,837 , \delta= 0.1 ,runs= 5');
epsilon_samples=[0; epsilon_samples; 0.15]
set(gca,'XTickLabel',epsilon_samples);set(gca,'XGrid','off','YGrid','on','ZGrid','off');
xlim([1 9]);
ylim([.1E-4 .03]);
set(gca,'yscale','log')
figureHandle = gcf;set(findall(figureHandle,'type','text'),'fontSize',12,'fontWeight','bold')
