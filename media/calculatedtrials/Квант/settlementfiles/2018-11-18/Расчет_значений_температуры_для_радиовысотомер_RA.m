clear;

% ����� ������ 2D �����
% data = (-10+25*rand(50,2));
% data = real(data.^rand(50,2));

load pointsForLineFitting.mat
plot(points(:,1),points(:,2),'o');
hold on

% ���
modelLeastSquares = polyfit(points(:,1),points(:,2),1); % p = polyfit(x,y,n) ���������� ������������ ��� ��������������� p(x) 
                                                        % �� ������� n ��� - ������ �������� (� ������ ���������� ���������) ��� ������ � y.
x = [min(points(:,1)) max(points(:,1))];
y = modelLeastSquares(1)*x + modelLeastSquares(2); % ��������� ������
plot(x,y,'r-')

% RANSAC
sampleSize = 2; % ����������� ����� �������
maxDistance = 2; % ������������ ���������� ��� ����� inlier

fitLineFcn = @(points) polyfit(points(:,1),points(:,2),1); % ������� �������� ��������� polyfit
evalLineFcn = ...   % ������� ������ ���������� (��������� ���������� �� ����� �� ������)
  @(model, points) sum((points(:, 2) - polyval(model, points(:,1))).^2,2);

[modelRANSAC, inlierIdx] = ransac(points,fitLineFcn,evalLineFcn, ... % ������� ������ ��� ������ RANSAC
  sampleSize,maxDistance); 

modelInliers = polyfit(points(inlierIdx,1),points(inlierIdx,2),1); % ��������� ������������ ��� ����� inlier

inlierPts = points(inlierIdx,:);
x = [min(inlierPts(:,1)) max(inlierPts(:,1))];
y = modelInliers(1)*x + modelInliers(2); % ��������� ������
plot(x, y, 'g-')
legend('������ �����','���','RANSAC');
hold off

