import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from lmfit import Model

# 정의할 함수
def function(x, A1, A2, x0, p):
    result = (A1 - A2) / (1 + (x / x0)**p) + A2
    return np.nan_to_num(result)  # 계산된 결과에서 NaN 값을 0으로 변환합니다.

# 데이터를 읽어올 파일 경로
e = 'C:/Users/pjy03/Downloads/실험결과_FAM 증폭/DuxC21A0063_2022-05-25_14-44-02.xlsx'
# Pandas를 사용하여 Excel 파일을 읽어옵니다.
df = pd.read_excel(e)

# 분석할 데이터가 있는 열의 라벨
selected_columns_labels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]

# 그래프를 그리기 위해 새로운 그림(figure)을 생성합니다.
plt.figure(figsize=(10, 6))

# 각 열에 대해 반복하면서 데이터를 처리하고 그래프를 그립니다.
for label in selected_columns_labels:
    # y_data : 각 사이클에서의 밝기값
    y_data = df[label].values
    # x_data : 사이클 번호
    x_data = np.arange(len(y_data))

    # lmfit 모델을 생성합니다.
    model = Model(function)

    # 모델의 파라미터를 초기화
    params = model.make_params(A1=max(y_data), A2=min(y_data), x0=len(y_data)/2, p=1)
    params['p'].set(min=0)  # p값의 최소값을 0으로 설정

    # 모델 fitting
    result = model.fit(y_data, params, x=x_data)

    # y축 범위를 설정
    plt.ylim(0, max(df[selected_columns_labels].values.max(axis=0)))

    plt.plot(x_data, result.best_fit, label=label)

# 범례 추가
plt.legend()
# x축과 y축의 라벨 설정
plt.xlabel('Cycle')
plt.ylabel('Brightness')
plt.grid(True)  # 그리드 추가
# 그래프를 화면에 보여줍니다.
plt.show()
