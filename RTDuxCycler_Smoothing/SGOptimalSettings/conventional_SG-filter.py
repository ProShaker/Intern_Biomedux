from def_AdaptiveSGfilter import *

# 엑셀 파일에서 확인한 열의 이름을 리스트로 저장
# ['12', '13', ..]
start = 12
end = 15
col_head = [str(i) for i in range(start, end+1)]

# first SG 필터의 매개변수
first_window_size = [7, 9, 11, 13, 15]  # 윈도우 크기, 보통 홀수를 사용
first_polynomial_order = [1, 2, 3]  # 다항식의 차수

# 엑셀 파일 경로
excel_file = 'C:/Users/KimHyeongJun/Desktop/바이오메듀스/데이터/PCR_CURVE_DATA(240104).xlsx'

# 엑셀 파일에서 지정된 열의 데이터 읽기
df_origin = pd.read_excel(excel_file, names=col_head)

# 열 개수를 저장하는 리스트
col_num = df_origin.shape[1]

# 원본, 필터링된 데이터를 저장하기 위한 리스트 선언

#각 열마다 데이터를 저장할 2차원 리스트
C_y1 = [[] for _ in range(col_num)]

# 다항식 차수와 Window Length별로 SG필터링을 적용하기 위해 4차원 리스트 생성
C_y1_filtered = [[copy.deepcopy(C_y1) for _ in range(len(first_polynomial_order))]
                                      for _ in range(len(first_window_size))]

# 필터링 데이터를 판다스 데이터 프레임으로 변환할 리스트
df_FSmoothing = [[copy.deepcopy(C_y1) for _ in range(len(first_polynomial_order))]
                                      for _ in range(len(first_window_size))]

# 각 well(12, 13..)의 데이터를 2차원 리스트에 저장
for i in range(len(col_head)):
    C_y1[i] = df_origin[col_head[i]].values.tolist()

# 각 열에 대해 conventional SG 필터 적용
for i in range(len(first_window_size)):
    for j in range(len(first_polynomial_order)):
        for k in range(len(C_y1)):
            C_y1_filtered[i][j][k] = savgol_filter(C_y1[k], first_window_size[i], first_polynomial_order[j])

# 샘플 데이터프레임 생성
for i in range(len(first_window_size)):
    for j in range(len(first_polynomial_order)):
            df_FSmoothing[i][j] = pd.DataFrame(columns=col_head)
            print(df_FSmoothing[i][j])
            df_FSmoothing[i][j][col_head[0]] = C_y1_filtered[i][j][0]
            df_FSmoothing[i][j][col_head[1]] = C_y1_filtered[i][j][1]
            df_FSmoothing[i][j][col_head[2]] = C_y1_filtered[i][j][2]
            df_FSmoothing[i][j][col_head[3]] = C_y1_filtered[i][j][3]

# 시트마다 데이터 작성
with pd.ExcelWriter(excel_file) as writer:
    df_origin.to_excel(writer, sheet_name='origin data.xlsx', index=False)
    for i in range(len(first_window_size)):
        for j in range(len(first_polynomial_order)):
                df_FSmoothing[i][j].to_excel(writer, sheet_name=
                'smoothing_'+str(first_window_size[i])+'_'+str(first_polynomial_order[j]), index=False)
                print(df_FSmoothing[i][j])

