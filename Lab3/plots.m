average = [23.228, 15.644, 13.502, 12.479, 9.654, 6.279, 5.844, 3.841, 3.486];
rtt = [13, 35, 68, 73, 49, 33, 135, 326, 322];


figure(1);
plot(log(rtt), log(average), '*');
figure(2);
plot((rtt), (average), '*');

%% 

transfered = [108851134, 90435681, 57971584, 32000012, 32557334, 27199361, 26329578, 38834490, 23571761, 36252962];
rtt = [40, 36, 100, 68, 31, 33, 122, 146, 74, 66];
duration = [58, 58, 53, 29, 35, 31, 31, 56, 35, 55];

average = 8.* (transfered ./ duration);

figure(1);
plot(log(rtt), log(average), '*');
figure(2);
plot((rtt), (average), '*');