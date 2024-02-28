import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar
from lmfit import Model

def function(x, A1, A2, x0, p):
    result = (A1 - A2) / (1 + (x / x0)**p) + A2
    return np.nan_to_num(result)

#이계도 함수
def second_derivative(x, A1, A2, x0, p):
    term1 = (A1 - A2) * p * (p - 1) * x**(p - 2)
    term2 = x0**2 * (1 + (x / x0)**p)**2
    term3 = (p * x**p) / (x0**p * (1 + (x / x0)**p)) - 1
    result = (term1 / term2) * term3
    return np.nan_to_num(result)

#파일 경로
directory_path = 'C:/Users/KimHyeongJun/Desktop/바이오메듀스/데이터/원본 데이터/LabG CTNG 결과/Negative/'

cnt = 0
#그 파일에서 엑셀 파일만 배열로 생성
file_list = [f for f in os.listdir(directory_path) if f.endswith('.xlsx')]
print(cnt)
results = []

for file_name in file_list:
    file_path = os.path.join(directory_path, file_name)
    df = pd.read_excel(file_path)
    print(cnt)

    selected_columns_labels = ['FAM', 'HEX', 'ROX', 'CY5']
    print(cnt)

    plt.figure(figsize=(10, 6))

    for label in selected_columns_labels:
        y_data = df[label].values
        x_data = np.linspace(1, len(y_data), len(y_data))
        print(x_data)
        model = Model(function)

        #변수들 초기값 설정
        params = model.make_params(A1=max(y_data), A2=min(y_data), x0=len(y_data)/2, p=2)
        params['p'].set(min=0.1)

        #모델 최적화
        result = model.fit(y_data, params, x=x_data)
        plt.ylim(0, max(df[selected_columns_labels].values.max(axis=0)))
        plt.plot(x_data, result.best_fit, label=label)

        #최적화한 변수 값 저장
        optimal_params = result.params.values()

        #이계도함수에서 최댓값이 나오는 x값과 함숫값 저장
        ct = minimize_scalar(lambda x: -second_derivative(x, *optimal_params), bounds=(6, len(y_data))).x
        ct_value = result.eval(x=ct)

        #그 x값이 10 초과, 44 미만일 때 출력
        if 10 < ct < 44:
            print(f"{label} ({file_name}): {ct}")
            plt.scatter(ct, ct_value, c='red', label=f'{label} : {ct}')

        else:
            print(f"{label} ({file_name}): Negative")
    print(cnt)

    plt.legend()
    plt.xlabel('Cycle')
    plt.ylabel('Brightness')
    plt.show()
    print('---------------------------------------------------------------------------')
