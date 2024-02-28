from def_AdaptiveSGfilter import *

start = 1
end = 25
col_head = [str(i) for i in range(start, end+1)]

# first SG 필터의 매개변수
first_window_size = [11]  # 윈도우 크기, 보통 홀수를 사용합니다.
first_polynomial_order = [1, 2, 3]  # 다항식의 차수

# 엑셀 파일 경로
excel_file = 'C:/Users/KimHyeongJun/Desktop/바이오메듀스/데이터/실험결과_FAM 증폭/DuxC21A0063_2022-05-25_14-44-02.xlsx'

# 엑셀 파일에서 데이터 읽기
df_origin = pd.read_excel(excel_file, names=col_head)

# well 개수를 저장하는 리스트
col_num = df_origin.shape[1]

# 원본, 필터링된 데이터를 저장하기 위한 리스트 선언
C_y1 = [[] for _ in range(col_num)]
C_y1_filtered = [[copy.deepcopy(C_y1) for _ in range(len(first_polynomial_order))] for _ in range(len(first_window_size))]
df_FSmoothing = [[copy.deepcopy(C_y1) for _ in range(len(first_polynomial_order))] for _ in range(len(first_window_size))]


# 각 well의 데이터를 2차원 리스트에 저장
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
        for k in range(len(C_y1)):
            df_FSmoothing[i][j][col_head[k]] = C_y1_filtered[i][j][k]
print("스무딩 데이터 길이 : ",len(df_FSmoothing))

# 시트마다 데이터 작성
with pd.ExcelWriter(excel_file) as writer:
    df_origin.to_excel(writer, sheet_name='origin data.xlsx', index=False)
    for i in range(len(first_window_size)):
        for j in range(len(first_polynomial_order)):
                df_FSmoothing[i][j].to_excel(writer, sheet_name=
                'smoothing_'+str(first_window_size[i])+'_'+str(first_polynomial_order[j]), index=False)
                print(df_FSmoothing[i][j])