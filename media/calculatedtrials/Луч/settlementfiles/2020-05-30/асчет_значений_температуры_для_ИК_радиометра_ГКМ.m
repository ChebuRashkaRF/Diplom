clear;
% �������� �����������
[mai, map]=(imread('mai.png', 'png'));
colormap(map);

% ����������� ��������� �����������
figure(1);
% subplot(3,2,1);
imshow(mai, map);
% gtext('�������� �����������');

% ����� ������
figure(2);
% subplot(3,2,2);
BW=edge(mai, 'sobel');
imshow(BW);
% gtext('����� ������');

% ����� ��������
figure(3);
% subplot(3,2,3);
BW=edge(mai, 'prewitt');
imshow(BW);
% gtext('����� ��������');

% ����� ��������
figure(4);
% subplot(3,2,4);
BW=edge(mai, 'roberts');
imshow(BW);
% gtext('����� ��������');

% ����� �����-���������
figure(5);
% subplot(3,2,5);
BW=edge(mai, 'log');
imshow(BW);
% gtext('����� �����-���������');

% ����� ����� 
figure(6);
% subplot(3,2,6);
BW=edge(mai, 'canny');
imshow(BW);
% gtext('����� ����� ');
