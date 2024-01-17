from def_AdaptiveSGfilter import *

# # txt 파일에서 추출할 열의 이름(헤드)
# col_head = ['Time;'FAM', 'HEX', 'ROX', 'CY5']

# 스무딩할 txt 파일의 이름
file_name_list = [
    'log000020-pd20231027-1502-49',
    'log000020-pd20231027-1718-49',
    'log000020-pd20231030-0940-03',
    'log000020-pd20231030-1339-08',
    'log000020-pd20231030-1532-39',
    'log000020-pd20231031-1548-16'
]

# SG 필터의 매개변수
window_size = [11]  # 윈도우 크기, 보통 홀수를 사용합니다.
polynomial_order = [1, 2, 3]  # 다항식의 차수

# 파일마다 스무딩을 진행하기 위해
for file_name in file_name_list:
    # 엑셀 파일 경로
    txt_file = 'C:/Users/KimHyeongJun/Desktop/바이오메듀스/데이터/LabG CTNG 결과/LabG20 그래프문제/'+file_name+'.txt'

    # txt 파일에서 데이터 읽어와서 판다스 데이터프레임으로 변환
    df_origin = pd.read_csv(txt_file, sep='\t', index_col=None)

    col_num = df_origin.shape[1]     # well 개수를 저장하는 리스트
    col_head = df_origin.columns     # 데이터의 열 제목을 저장하는 리스트

    # 필터링된 데이터를 저장하기 위한 리스트 선언
    C_y1 = [[] for _ in range(col_num)]
    C_y1_filtered = [[copy.deepcopy(C_y1) for _ in range(len(polynomial_order))] for _ in range(len(window_size))]
    df_FSmoothing = [[copy.deepcopy(C_y1) for _ in range(len(polynomial_order))] for _ in range(len(window_size))]

    # 각 well의 데이터를 2차원 리스트에 저장
    for i, column in enumerate(col_head):
        C_y1[i] = df_origin[column].values.tolist()

    # 각 열에 대해 conventional SG 필터 적용
    for i in range(len(window_size)):
        for j in range(len(polynomial_order)):
            for k in range(len(C_y1)):
                # cycle과 time은 필터를 적용하면 안 되기 때문에 if 문으로 구분
                if k <= 1:
                    C_y1_filtered[i][j][k] = C_y1[k]
                else :
                    C_y1_filtered[i][j][k] = savgol_filter(C_y1[k], window_size[i], polynomial_order[j])

    # 샘플 데이터프레임 생성
    for i in range(len(window_size)):
        for j in range(len(polynomial_order)):
            df_FSmoothing[i][j] = pd.DataFrame(columns=col_head)
            for k in range(len(C_y1)):
                df_FSmoothing[i][j][col_head[k]] = C_y1_filtered[i][j][k]
    print("스무딩 데이터 길이 : ",df_FSmoothing)

    # 시트마다 데이터 작성
    with pd.ExcelWriter(excel_file) as writer:
        df_origin.to_excel(writer, sheet_name='origin data.xlsx', index=False)
        for i in range(len(window_size)):
            for j in range(len(polynomial_order)):
                    df_FSmoothing[i][j].to_excel(writer, sheet_name=
                    'smoothing_'+str(window_size[i])+'_'+str(polynomial_order[j]), index=False)
                    print(df_FSmoothing[i][j])