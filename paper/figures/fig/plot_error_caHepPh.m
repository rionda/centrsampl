Y_1 = [
0.00013497170279464703
0.0003090190978901827
0.002118440718324583
];
plot(1,Y_1(1),'rs','Linewidth',2);hold on;plot(1,Y_1(2),'mV','Linewidth',2);hold on;plot(1,Y_1(3),'O','Linewidth',2);
Y_2 = [
0.00020254324559134372
0.0004635569639890202
0.0019085633098387903
];
plot(2,Y_2(1),'rs','Linewidth',2);hold on;plot(2,Y_2(2),'mV','Linewidth',2);hold on;plot(2,Y_2(3),'O','Linewidth',2);
Y_3 = [
0.00027310747873600426
0.000629219230743718
0.002926247012692734
];
plot(3,Y_3(1),'rs','Linewidth',2);hold on;plot(3,Y_3(2),'mV','Linewidth',2);hold on;plot(3,Y_3(3),'O','Linewidth',2);
Y_4 = [
0.0005241064555142115
0.0012513464452645754
0.006574189050764609
];
plot(4,Y_4(1),'rs','Linewidth',2);hold on;plot(4,Y_4(2),'mV','Linewidth',2);hold on;plot(4,Y_4(3),'O','Linewidth',2);
Y_5 = [
0.0007646074667535152
0.001875361831674983
0.008832662108307441
];
plot(5,Y_5(1),'rs','Linewidth',2);hold on;plot(5,Y_5(2),'mV','Linewidth',2);hold on;plot(5,Y_5(3),'O','Linewidth',2);
Y_6 = [
0.0009953217031577416
0.002593287841552609
0.014566946169924766
];
plot(6,Y_6(1),'rs','Linewidth',2);hold on;plot(6,Y_6(2),'mV','Linewidth',2);hold on;plot(6,Y_6(3),'O','Linewidth',2);
Y_7 = [
0.001167059118422652
0.003219449000430563
0.017143404236966378
];
plot(7,Y_7(1),'rs','Linewidth',2);hold on;plot(7,Y_7(2),'mV','Linewidth',2);hold on;plot(7,Y_7(3),'O','Linewidth',2);
epsilon_samples = {
%'0.005(146052)'
'0.01(36513)'
'0.015(16228)'
'0.02(9129)'
'0.04(2283)'
'0.06(1015)'
'0.08(571)'
'0.1(366)'
};
legend('Avg (diam-2approx)','Avg+Stddev (diam-2approx)','Max (diam-2approx)', 'Location', 'SouthEast');
set(gca, 'YScale', 'log'); xlabel('epsilon (sample size)'); 
ylabel('Absolute estimation error');title('ca-HepPh-u , |V|=12.008 , |E|=237.010 , \delta= 0.1 ,runs= 5');
epsilon_samples=[0; epsilon_samples; 0.15]
set(gca,'XTickLabel',epsilon_samples);set(gca,'XGrid','off','YGrid','on','ZGrid','off');
xlim([0 8]);
ylim([.0001 .03]);
set(gca,'yscale','log')
figureHandle = gcf;set(findall(figureHandle,'type','text'),'fontSize',12,'fontWeight','bold')
