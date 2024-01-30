from def_AdaptiveSGfilter import *
from scipy.signal import argrelextrema, argrelmin

#==============step1. conventional SG필터 적용==================

# first SG 필터의 매개변수
first_window_size = [1, 3, 5, 7, 9, 11, 13, 15]  # 윈도우 크기, 보통 홀수를 사용합니다.
first_polynomial_order = [1, 2, 3, 4, 5]  # 다항식의 차수

# 데이터에 스케일러 적용
# C_y1 = scaler.fit_transform(C_y1)
C_y_d2 = []

# 각 열에 대해 conventional SG 필터 적용
C_y1_filtered = savgol_filter(C_y1, first_window_size, first_polynomial_order)
print("C_y1_filtered : ", C_y1_filtered)

data = np.array(C_y1_filtered)

# 지역 최대값 찾기
local_max = argrelextrema(data, np.greater)
print("Local maxima index:", local_max)

# 지역 최소값 찾기
local_min = argrelmin(data, np.less)
print("Local minima index:", local_min)

for i in range(len(C_y1_filtered)-1):
    C_y_d2.append(C_y1_filtered[i+1] - C_y1_filtered[i])

k1, M1 = fuzzyRelation(C_y_d2)
print("===========k1, M1=========", k1, M1)
print(savgol_filter(C_y1_filtered, M1, k1))

#==============step2. local extrema 판별, distance 계산==================
#==============step3. R값 결정==================

# 0번 인덱스를 제외한 최솟값을 기준으로 signal을 나눔
C_y1_filtered = SeparationRound(C_y1_filtered)

# distance벡터가 C_y1_filtered의 구간 내 거리를 저장하도록 2차원배열로 선언
C_y_d = [[] for _ in range(len(C_y1_filtered))]

# 나눠진 구간에 대해 distance 계산
for i in range(len(C_y1_filtered)):
    for j in range(len(C_y1_filtered[i])-1):
        C_y_d[i].append(C_y1_filtered[i][j+1]-C_y1_filtered[i][j])
print("distance 벡터 : ", C_y_d)


# !!유의점 : 여기서 이미 두 어레이에 대해 k=5가 나옴 선형적인 앞부분에서 다항식 차수로 5가 나왔다는 거에 유의
#==============나눈 구간에 대해 Polynomial degree, Window Length 구함=========
for i in range(len(C_y1_filtered)):
    k, M = fuzzyRelation(C_y_d[i])
    print("k = ", k)
    print("M = ", M)

    polynomial_order.append(k)
    window_size.append(M)

    print(polynomial_order)
    print(window_size)

#==============adaptive SG-smoothing 적용=========

for i in range(len(C_y1_filtered)):
    C_y1_filtered2.append(savgol_filter(C_y1_filtered[i], window_size[i], polynomial_order[i]))
print(len(C_y1))
print(len(C_y1_filtered))
print(len(C_y1_filtered2))

plt.plot(C_cycle, C_y1)
plt.title('My Graph1')  # 그래프 제목 설정
plt.xlabel('X')  # x축 라벨 설정
plt.ylabel('Y')  # y축 라벨 설정
plt.show()

plt.plot(C_cycle, C_y1_filtered)
plt.title('My Graph2')  # 그래프 제목 설정
plt.xlabel('X')  # x축 라벨 설정
plt.ylabel('Y')  # y축 라벨 설정
plt.show()

plt.plot(C_cycle, C_y1_filtered2)
plt.title('My Graph3')  # 그래프 제목 설정
plt.xlabel('X')  # x축 라벨 설정
plt.ylabel('Y')  # y축 라벨 설정
plt.show()