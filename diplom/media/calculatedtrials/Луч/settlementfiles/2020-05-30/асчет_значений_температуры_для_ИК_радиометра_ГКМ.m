clear;
% загрузка изображения
[mai, map]=(imread('mai.png', 'png'));
colormap(map);

% отображение исходного изображения
figure(1);
% subplot(3,2,1);
imshow(mai, map);
% gtext('исходное изображение');

% метод Собеля
figure(2);
% subplot(3,2,2);
BW=edge(mai, 'sobel');
imshow(BW);
% gtext('метод Собеля');

% метод Превитта
figure(3);
% subplot(3,2,3);
BW=edge(mai, 'prewitt');
imshow(BW);
% gtext('метод Превитта');

% метод Робертса
figure(4);
% subplot(3,2,4);
BW=edge(mai, 'roberts');
imshow(BW);
% gtext('метод Робертса');

% метод Марра-Хильдрета
figure(5);
% subplot(3,2,5);
BW=edge(mai, 'log');
imshow(BW);
% gtext('метод Марра-Хильдрета');

% метод Канни 
figure(6);
% subplot(3,2,6);
BW=edge(mai, 'canny');
imshow(BW);
% gtext('метод Канни ');
