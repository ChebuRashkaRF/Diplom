clear;

% набор шумных 2D точек
% data = (-10+25*rand(50,2));
% data = real(data.^rand(50,2));

load pointsForLineFitting.mat
plot(points(:,1),points(:,2),'o');
hold on

% МНК
modelLeastSquares = polyfit(points(:,1),points(:,2),1); % p = polyfit(x,y,n) возвращает коэффициенты для полиномиального p(x) 
                                                        % из степени n это - лучшая подгонка (в смысле наименьших квадратов) для данных в y.
x = [min(points(:,1)) max(points(:,1))];
y = modelLeastSquares(1)*x + modelLeastSquares(2); % уравнение прямой
plot(x,y,'r-')

% RANSAC
sampleSize = 2; % минимальный объем выборки
maxDistance = 2; % максимальное расстояние для точек inlier

fitLineFcn = @(points) polyfit(points(:,1),points(:,2),1); % функция подгонки используя polyfit
evalLineFcn = ...   % функция оценки расстояния (вычисляет расстояние от точки до прямой)
  @(model, points) sum((points(:, 2) - polyval(model, points(:,1))).^2,2);

[modelRANSAC, inlierIdx] = ransac(points,fitLineFcn,evalLineFcn, ... % функция матлаб для метода RANSAC
  sampleSize,maxDistance); 

modelInliers = polyfit(points(inlierIdx,1),points(inlierIdx,2),1); % получение коэффицентов для точек inlier

inlierPts = points(inlierIdx,:);
x = [min(inlierPts(:,1)) max(inlierPts(:,1))];
y = modelInliers(1)*x + modelInliers(2); % уравнение прямой
plot(x, y, 'g-')
legend('шумные точки','МНК','RANSAC');
hold off

