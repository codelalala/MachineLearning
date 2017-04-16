% data=load('statistics.txt');
% figure(1)
% plot(data(:,1),data(:,2))
% mean(data(:,2))
% saveas(figure(1),'fitZ.jpg')
% figure(2)
% plot(data(:,1),data(:,3))
% saveas(figure(2),'average_length.jpg')
% figure(3)
% plot(data(:,1),data(:,4))
% saveas(figure(3),'total_Z_bound_within_cluster.jpg')
% figure(4)
% plot(data(:,1),data(:,5))
% saveas(figure(4),'annealing_bound.jpg')
% figure(5)
% plot(data(:,1),data(:,6))
% saveas(figure(5),'lateral_bound.jpg')
% figure(6)
% plot(data(:,1),data(:,7))
% saveas(figure(6),'lateral_bound_TT.jpg')
% figure(7)
% plot(data(:,1),data(:,8))
% saveas(figure(7),'lateral_bound_TD.jpg')
% figure(8)
% plot(data(:,1),data(:,9))
% saveas(figure(8),'lateral_bound_DD.jpg')
% figure(9)
% plot(data(:,1),data(:,10)./data(:,11))
% saveas(figure(9),'TD_ratio.jpg')
% figure(10)
% plot(data(:,1),data(:,12))
% saveas(figure(10),'TT_bound.jpg')
% figure(11)
% plot(data(:,1),data(:,13))
% saveas(figure(11),'TD_bound.jpg')
% figure(12)
% plot(data(:,1),data(:,14))
% saveas(figure(12),'DD_bound.jpg')
% figure(13)
% plot(data(:,1),data(:,15))
% saveas(figure(13),'average_lifetime.jpg')
%myprofile
data=load('statistics.txt');
%data=load('statistics - Copy.txt');

figure(1)
subplot(3,3,1)
time_series=data(:,1);
FtsZ_in_the_cytoplasm=data(:,2);
master_sheet{locator,42}=time_series;
master_sheet{locator,45}=FtsZ_in_the_cytoplasm;
master_sheet{locator,44}=num_ftsz_in_ring;
plot(data(:,1),data(:,2))
hold on
plot(time_series_output,num_ftsz_in_ring)
hold off
xlabel('number of FtsZ', 'fontsize', 8)
subplot(3,3,2)
FtsZ_GTP=data(:,10);
FtsZ_GDP=data(:,11);
master_sheet{locator,49}=FtsZ_GTP;
master_sheet{locator,50}=FtsZ_GDP;
plot(data(:,1),data(:,10)./data(:,11))
xlabel('ratio of FtsZ-GTP/FtsZ-GDP', 'fontsize', 8)
subplot(3,3,3)
lateral_bound=data(:,6);
master_sheet{locator,54}=lateral_bound;
plot(data(:,1),data(:,6))
xlabel('number of lateral bounds', 'fontsize', 8)
% subplot(3,3,4)
% polymer_bound=data(:,12)+data(:,13)+data(:,14);
% master_sheet{locator,53}=polymer_bound;
% plot(data(:,1),polymer_bound)
% xlabel('number of polymer bounds', 'fontsize', 8)
subplot(3,3,5)
average_length=data(:,3);
master_sheet{locator,55}=average_length;
plot(data(:,1),average_length)
xlabel('polymer average length', 'fontsize', 8)
master_sheet{locator,43}=time_series_output;


subplot(3,3,6)
master_sheet{locator,46}=width;
plot(time_series_output,width);
xlabel('ring width', 'fontsize', 8)

subplot(3,3,7)
master_sheet{locator,47}=length_of_ring;
plot(time_series_output,length_of_ring);
xlabel('ring length', 'fontsize', 8)

subplot(3,3,8)
master_sheet{locator,51}=number_of_up./(number_of_up+number_of_down);
master_sheet{locator,52}=number_of_down./(number_of_up+number_of_down);
plot(time_series_output,master_sheet{locator,51});
hold on
plot(time_series_output,master_sheet{locator,52});
hold off
xlabel('pencentage of up/down pointing FtsZ', 'fontsize', 8)