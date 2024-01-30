import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
import copy
import matplotlib.pyplot as plt
import os
from scipy.optimize import minimize_scalar
from lmfit import Model

def function(x, A1, A2, x0, p):
    result = (A1 - A2) / (1 + (x / x0)**p) + A2
    # print('result :', f'{result}')
    return np.nan_to_num(result)

#이계도 함수
def second_derivative(x, A1, A2, x0, p):
    # 값이 0 또는 음수인 경우를 방지
    x = np.clip(x, a_min=0.0001, a_max=None)  # x의 최소값을 0.0001로 설정
    x0 = np.clip(x0, a_min=0.0001, a_max=None)  # x0의 최소값을 0.0001로 설정
    p = np.clip(p, a_min=0.0001, a_max=None)  # p의 최소값을 0.0001로 설정

    term1 = (A1 - A2) * p * (p - 1) * x**(p - 2)
    # print('term1 :', f'{term1}')

    term2 = x0**2 * (1 + (x / x0)**p)**2
    # print('term2 :', f'{term2}')

    term3 = (p * x**p) / (x0**p * (1 + (x / x0)**p)) - 1
    # print('term3 :', f'{term3}')

    result = (term1 / term2) * term3
    # print('result :', f'{result}')

    return np.nan_to_num(result)


def detect_CT(y_data):

    x_data = np.linspace(1, len(y_data), len(y_data))

    model = Model(function)

    # 변수들 초기값 설정
    params = model.make_params(A1=max(y_data), A2=min(y_data), x0=len(y_data) / 2, p=2)
    params['p'].set(min=0.1)
    # print(f"A1 : {max(y_data)} ")
    # print(f"A2 : {min(y_data)} ")
    # print(f"x0 : {len(y_data)} ")
    # print(f"p : {params['p']} ")

    # 모델 최적화
    result = model.fit(y_data, params, x=x_data)

    # 최적화한 변수 값 저장
    optimal_params = result.params.values()

    # 이계도함수에서 최댓값이 나오는 x값과 함숫값 저장
    ct = minimize_scalar(lambda x: -second_derivative(x, *optimal_params), bounds=(6, len(y_data))).x
    # ct_value = result.eval(x=ct)
    if 10 < ct < 39:
        ct_value = y_data[np.abs(x_data - ct).argmin()]
    else:
        ct_value = 0
    return ct, ct_value

# ======== Adaptive Sg필터링에 적용되는 부분
# # Cutting point를 기준으로 구간을 나눠주는 함수
# def SeparationRound(y):
#     min_value = np.min(y[1:])
#     min_index = np.where(y == min_value)[0][0] + 1
#     R = min_index
#     return [y[:min_index], y[min_index-1:]]
#
# # fuzzy relation 으로 Polynomial degree, Window Length 구하는 함수
# def fuzzyRelation(distance_array):
#     max_value = max(distance_array)
#     mean_value = sum(distance_array) / len(distance_array) #구간 R에 대해 points들의 평균 거리
#     number_of_sample = len(distance_array)
#
#     num = 1/ (1+math.exp(mean_value-max_value))
#     print(max_value)
#     print(mean_value)
#     print(num)
#
#     if 1.0 >= num > 0.9:
#         k = 5
#         M = round(0.3*mean_value)
#     elif 0.89 >= num > 0.75:
#         k = 4
#         M = round(0.5*mean_value)
#     elif 0.75 >= num > 0.45:
#         k = 3
#         M = round(mean_value)
#     elif 0.44 >= num > 0.2:
#         k = 2
#         M = round(0.5*number_of_sample)
#     else:
#         k=1
#         M = round(0.8*number_of_sample)
#     return k, M

