import numpy as np
import matplotlib.pyplot as plt
from lmfit import Model

# 주어진 함수 정의
def function(x, A1, A2, x0, p):
    result = (A1 - A2) / (1 + (x / x0)**p) + A2
    return np.nan_to_num(result)  # NaN 값이나 무한대 값이 있으면 0으로 변환

# y값 데이터 정의
y_data = np.array([
    30.24703633, 44.01453155, 44.06832377, 42.6652645, 42.6749522, 42.50873168,
    42.56685787, 42.02536648, 42.76456342, 42.87571702, 42.7292543, 42.98495857,
    42.76532823, 42.36775016, 41.57131931, 42.45787126, 42.21363926, 41.0387508,
    41.49356278, 41.32402804, 41.33919694, 40.9848311, 41.22919057, 41.02829828,
    41.99604844, 43.93550032, 46.88183556, 52.27966858, 59.70248566, 69.59005736,
    80.4972594, 92.69585723, 102.1555131, 112.7701721, 121.5899299, 130.204334,
    137.0532823, 143.1460803, 148.6493308, 153.0806883, 157.1366475
])

# x값 데이터 정의
x_data = np.arange(len(y_data))  # y_data의 길이만큼의 일련번호 배열 생성

# 모델 생성
model = Model(function)

# 파라미터 초기값 설정
params = model.make_params(A1=max(y_data), A2=min(y_data), x0=len(y_data)/2, p=1)
params['p'].set(min=0)  # 'p' 파라미터의 최소값을 0으로 설정

# 모델 fitting 수행
result = model.fit(y_data, params, x=x_data)

# fitting 결과 출력
print(result.fit_report())

# fitting 그래프 출력
result.plot_fit()
plt.grid(True)  # 그리드 추가
plt.show()
