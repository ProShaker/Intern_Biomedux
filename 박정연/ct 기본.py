import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from lmfit import Model
from scipy.optimize import minimize_scalar

# sigmoid 함수에 fitting할 함수 정의
def function(x, A1, A2, x0, p):
    result = (A1 - A2) / (1 + (x / x0) ** p) + A2
    return np.nan_to_num(result)  # NaN 값이나 무한대 값이 있으면 0으로 변환

# 이계도함수 정의
def second_derivative(x, A1, A2, x0, p):
    # 도함수의 각 항 정의
    term1 = (A1 - A2) * p * (p - 1) * x ** (p - 2)
    term2 = x0 ** 2 * (1 + (x / x0) ** p) ** 2
    term3 = (p * x ** p) / (x0 ** p * (1 + (x / x0) ** p)) - 1

    # term2가 0 혹은 무한대인 경우를 체크
    if np.isinf(term2) or term2 == 0:
        return np.nan  # 적절한 값 반환

    result = (term1 / term2) * term3
    return np.nan_to_num(result)  # NaN 값이나 무한대 값이 있으면 0으로 변환

# 데이터를 읽어올 파일 경로
e = 'C:/Users/KimHyeongJun/Desktop/바이오메듀스/데이터/LabG CTNG 결과/LabG20 그래프문제/' + 'log000020-pd20231030-0940-03' + '.txt'

# 엑셀 파일 불러오기
df = pd.read_csv(e, sep='\t', index_col=None)
# Cycle이 6 이후인 데이터만 선택, 초반 spike를 무시하기 위해
df = df[df['Cycle'] > 5]
# 분석할 데이터가 있는 열의 라벨
selected_columns_labels = ['FAM', 'HEX', 'ROX', 'CY5']

# 그래프 그릴 figure 생성
plt.figure(figsize=(10, 6))

# 각 열에 대해 그래프 plot
for label in selected_columns_labels:

    # y_data : 각 사이클에서의 밝기값
    y_data = df[label].values

    # x_data : 사이클 번호
    x_data = np.arange(len(y_data))

    # lmfit 모델 생성
    model = Model(function)

    # 모델 파라미터 초기화합니다.
    params = model.make_params(A1=max(y_data), A2=min(y_data), x0=len(y_data)/2, p=1)
    params['p'].set(min=0)  # p값의 최소값을 0으로 설정합니다.

    # 데이터를 이용하여 모델을 적합시킵니다.
    result = model.fit(y_data, params, x=x_data)

    # 그래프의 y축 범위를 설정합니다.
    plt.ylim(0, max(df[selected_columns_labels].values.max(axis=0)))

    # 적합된 결과를 그래프에 그립니다.
    plt.plot(x_data, result.best_fit, label=label)

    # 최적화된 파라미터값을 얻습니다.
    optimal_params = result.params.values()

    # 두 번째 도함수의 최대값 위치를 찾습니다.
    max_x = minimize_scalar(lambda x: -second_derivative(x, *optimal_params)).x

    # 최대값 위치가 0과 45 사이에 있다면, 그 위치에 5를 더한 값을 출력하고,
    # 그렇지 않다면 Negative를 출력합니다.
    if 0 < max_x < 45:
        print(f"{label} : {max_x + 5}")
    else:
        print(f"{label} : Negative")

# 범례를 그림에 추가합니다.
plt.legend()
# x축과 y축의 라벨을 설정합니다.
plt.xlabel('Cycle')
plt.ylabel('Brightness')
plt.grid(True)
# 그래프를 화면에 보여줍니다.
plt.show()
