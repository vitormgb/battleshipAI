clear
clc
close all

hunter = dlmread('hunterStats.out',' ');
dummy = dlmread('dummyStats.out',' ');
probabilistic = dlmread('probabilisticStats.out',' ');
probabilisticHunter = dlmread('probabilisticHunterStats.out',' ');

shots_hunter = hunter(:,2);
misses_hunter = hunter(:,3);

shots_dummy = dummy(:,2);
misses_dummy = dummy(:,3);

shots_probabilistic = probabilistic(:,2);
misses_probabilistic = probabilistic(:,3);

shots_probabilistic_hunter = probabilisticHunter(:,2);
misses_probabilistic_hunter = probabilisticHunter(:,3);

num_shots_hunter = zeros(1,100);
num_misses_hunter = zeros(1,100);

num_shots_dummy = zeros(1,100);
num_misses_dummy = zeros(1,100);

num_shots_probabilistic = zeros(1,100);
num_misses_probabilistic = zeros(1,100);

num_shots_probabilistic_hunter = zeros(1,100);
num_misses_probabilistic_hunter = zeros(1,100);

for i=1:length(shots_hunter)
    num_shots_hunter(shots_hunter(i)) = num_shots_hunter(shots_hunter(i)) + 1;
    num_shots_dummy(shots_dummy(i)) = num_shots_dummy(shots_dummy(i)) + 1;
    num_shots_probabilistic(shots_probabilistic(i)) = num_shots_probabilistic(shots_probabilistic(i)) + 1;
    num_shots_probabilistic_hunter(shots_probabilistic_hunter(i)) = num_shots_probabilistic_hunter(shots_probabilistic_hunter(i)) + 1;
end
for i=1:length(misses_hunter)
    num_misses_hunter(misses_hunter(i)) = num_misses_hunter(misses_hunter(i)) + 1;
    num_misses_dummy(misses_dummy(i)) = num_misses_dummy(misses_dummy(i)) + 1;
    num_misses_probabilistic(misses_probabilistic(i)) = num_misses_probabilistic(misses_probabilistic(i)) + 1;
    num_misses_probabilistic_hunter(misses_probabilistic_hunter(i)) = num_misses_probabilistic_hunter(misses_probabilistic_hunter(i)) + 1;
end

mean_shots_hunter = mean(shots_hunter);
mean_misses_hunter = mean(misses_hunter);
mean_shots_dummy = mean(shots_dummy);
mean_misses_dummy = mean(misses_dummy);
mean_shots_probabilistic = mean(shots_probabilistic);
mean_misses_probabilistic = mean(misses_probabilistic);
mean_shots_probabilistic_hunter = mean(shots_probabilistic_hunter);
mean_misses_probabilistic_hunter = mean(misses_probabilistic_hunter);

index_shots_hunter = int32(mean_shots_hunter); 
index_misses_hunter = int32(mean_misses_hunter);
index_shots_dummy = int32(mean_shots_dummy); 
index_misses_dummy = int32(mean_misses_dummy);
index_shots_probabilistic = int32(mean_shots_probabilistic); 
index_misses_probabilistic = int32(mean_misses_probabilistic);
index_shots_probabilistic_hunter = int32(mean_shots_probabilistic_hunter);
index_misses_probabilistic_hunter = int32(mean_misses_probabilistic_hunter);

figure; 
plot(num_shots_hunter, 'k--', 'LineWidth', 2)
hold on
plot(num_shots_dummy, 'b--', 'LineWidth', 2)
plot(num_shots_probabilistic, 'r--', 'LineWidth', 2)
plot(num_shots_probabilistic_hunter, 'm--', 'LineWidth', 2)
plot(round(mean_shots_hunter), num_shots_hunter(index_shots_hunter), 'kx', 'LineWidth', 4)
plot(round(mean_shots_dummy), num_shots_dummy(index_shots_dummy), 'bx', 'LineWidth', 4)
plot(round(mean_shots_probabilistic), num_shots_probabilistic(index_shots_probabilistic), 'rx', 'LineWidth', 4)
plot(round(mean_shots_probabilistic_hunter), num_shots_probabilistic_hunter(index_shots_probabilistic_hunter), 'mx', 'LineWidth', 4)

str = ['(',num2str(mean_shots_hunter),',',num2str(num_shots_hunter(index_shots_hunter)),')', '\rightarrow'];
text(round(mean_shots_hunter),num_shots_hunter(index_shots_hunter),str,'HorizontalAlignment','right', 'FontSize', 12)
str = ['(',num2str(mean_shots_dummy),',',num2str(num_shots_dummy(index_shots_dummy)),')', '\rightarrow'];
text(round(mean_shots_dummy),num_shots_dummy(index_shots_dummy),str,'HorizontalAlignment','right', 'FontSize', 12)
str = ['\leftarrow','(',num2str(mean_shots_probabilistic),',',num2str(num_shots_probabilistic(index_shots_probabilistic)),')'];
text(round(mean_shots_probabilistic),num_shots_probabilistic(index_shots_probabilistic),str,'HorizontalAlignment','left', 'FontSize', 12)
str = ['\leftarrow','(',num2str(mean_shots_probabilistic_hunter),',',num2str(num_shots_probabilistic_hunter(index_shots_probabilistic_hunter)),')'];
text(round(mean_shots_probabilistic_hunter),num_shots_probabilistic_hunter(index_shots_probabilistic_hunter),str,'HorizontalAlignment','left', 'FontSize', 12)

leg = zeros(8,1);
leg(1) = plot(NaN, NaN, 'k--', 'LineWidth', 2);
leg(2) = plot(NaN, NaN, 'b--', 'LineWidth', 2);
leg(3) = plot(NaN, NaN, 'r--', 'LineWidth', 2);
leg(4) = plot(NaN, NaN, 'm--', 'LineWidth', 2);
leg(5) = plot(NaN, NaN, 'kx', 'LineWidth', 4);
leg(6) = plot(NaN, NaN, 'bx', 'LineWidth', 4);
leg(7) = plot(NaN, NaN, 'rx', 'LineWidth', 4);
leg(8) = plot(NaN, NaN, 'mx', 'LineWidth', 4);
ml = legend(leg, 'Hunter Player', 'Dummy Player', 'Probabilistic Player', 'Probabilistic Hunter Player', 'Average Number of Shots (Hunter)', 'Average Number of Shots (Dummy)', 'Average Number of Shots (Probabilistic)', 'Average Number of Shots (Probabilistic Hunter)', 'Location','northwest');
set(ml, 'FontSize', 14)
xlabel('Number of Shots', 'FontSize', 18)
ylabel('Number of Turns', 'FontSize', 18)
xlim([0 100])
ylim([0 18500])

figure; 
plot(num_misses_hunter, 'k--', 'LineWidth', 2)
hold on
plot(num_misses_dummy, 'b--', 'LineWidth', 2)
plot(num_misses_probabilistic, 'r--', 'LineWidth', 2)
plot(num_misses_probabilistic_hunter, 'm--', 'LineWidth', 2)
plot(round(mean_misses_hunter), num_misses_hunter(index_misses_hunter), 'kx', 'LineWidth', 4)
plot(round(mean_misses_dummy), num_misses_dummy(index_misses_dummy), 'bx', 'LineWidth', 4)
plot(round(mean_misses_probabilistic), num_misses_probabilistic(index_misses_probabilistic), 'rx', 'LineWidth', 4)
plot(round(mean_misses_probabilistic_hunter), num_misses_probabilistic_hunter(index_misses_probabilistic_hunter), 'mx', 'LineWidth', 4)

str = ['(',num2str(mean_misses_hunter),',',num2str(num_misses_hunter(index_misses_hunter)),')', '\rightarrow'];
text(round(mean_misses_hunter),num_misses_hunter(index_misses_hunter),str,'HorizontalAlignment','right','FontSize', 12)
str = ['(',num2str(mean_misses_dummy),',',num2str(num_misses_hunter(index_misses_dummy)),')', '\rightarrow'];
text(round(mean_misses_dummy),num_misses_dummy(index_misses_dummy),str,'HorizontalAlignment','right', 'FontSize', 12)
str = ['\leftarrow','(',num2str(mean_misses_probabilistic),',',num2str(num_misses_probabilistic(index_misses_probabilistic)),')'];
text(round(mean_misses_probabilistic),num_misses_probabilistic(index_misses_probabilistic),str,'HorizontalAlignment','left', 'FontSize', 12)
str = ['\leftarrow','(',num2str(mean_misses_probabilistic_hunter),',',num2str(num_misses_probabilistic_hunter(index_misses_probabilistic_hunter)),')'];
text(round(mean_misses_probabilistic_hunter),num_misses_probabilistic_hunter(index_misses_probabilistic_hunter),str,'HorizontalAlignment','left', 'FontSize', 12)
leg = zeros(8,1);
leg(1) = plot(NaN, NaN, 'k--', 'LineWidth', 2);
leg(2) = plot(NaN, NaN, 'b--', 'LineWidth', 2);
leg(3) = plot(NaN, NaN, 'r--', 'LineWidth', 2);
leg(4) = plot(NaN, NaN, 'm--', 'LineWidth', 2);
leg(5) = plot(NaN, NaN, 'kx', 'LineWidth', 4);
leg(6) = plot(NaN, NaN, 'bx', 'LineWidth', 4);
leg(7) = plot(NaN, NaN, 'rx', 'LineWidth', 4);
leg(8) = plot(NaN, NaN, 'mx', 'LineWidth', 4);
ml = legend(leg, 'Hunter Player', 'Dummy Player', 'Probabilistic Player', 'Probabilistic Hunter Player', 'Average Number of Missed Shots (Hunter)', 'Average Number of Missed Shots (Dummy)', 'Average Number of Missed Shots (Probabilistic)', 'Average Number of Missed Shots (Probabilistic Hunter)', 'Location','northwest');
set(ml, 'FontSize', 14)
xlabel('Number of Missed Shots', 'FontSize', 18)
ylabel('Number of Turns', 'FontSize', 18)
xlim([0 100])
ylim([0 18500])