clc; clear; close all;

% Initialization
cpi = [1.75 1.16 3.49 1.09 10.24];
exec = [87.5 58.2 174.7 54.4 513.6];
il1 = [0.0054 0.0145 0.0097 0.0019 0.0015];
dl1 = [1.4618 0.1669 6.0971 0.1955 12.1831];
l2 = [26.6550 8.1390 99.9967 72.6148 99.9979];

hold on;
plot(cpi, '-o', 'LineWidth', 2)
plot(il1 * 100, '-o')
plot(dl1, '-o')
plot(l2 / 50, '-o')
legend('CPI', 'L1 i-cache miss rate (x100)', 'L1 d-cache miss rate', 'L2 cache miss rate (/50)')
xticks(1:5)
xticklabels({'specbzip', 'spechmmer', 'sepclibm', 'specmcf', 'specsjeng'})
saveas(gcf, 'img/caches.jpg')

disp('Done!')