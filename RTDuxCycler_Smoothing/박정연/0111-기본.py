from def_AdaptiveSGfilter import *

file_path = 'C:/Users/KimHyeongJun/Desktop/바이오메듀스/데이터/원본 데이터/240129/'
save_path = 'C:/Users/KimHyeongJun/Desktop/바이오메듀스/데이터/LabG CTNG 결과/smoothing/fixed_2_7/240129/'

# txt 파일에서 데이터 읽어와서 판다스 데이터프레임으로 변환
df_origin = pd.read_csv(file_path + 'log000009-pd20240118-1544-46.txt', sep='\t', index_col=None)

# y값 데이터 정의
y_data = df_origin['FAM']
print(y_data)
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
