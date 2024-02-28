import matplotlib.pyplot as plt
from def_AdaptiveSGfilter import *

file_path = 'C:/Users/KimHyeongJun/Desktop/바이오메듀스/데이터/원본 데이터/LabG CTNG 결과/고농도/'
save_path = 'C:/Users/KimHyeongJun/Desktop/바이오메듀스/데이터/LabG CTNG 결과/smoothing/20이상/고농도/'

# 스무딩할 txt 파일의 이름
file_name_list = [
    'log000007-pd20231101-1129-51',
    'log000012-pd20231101-1333-29',
    'log000013-pd20231102-1524-50',
    'log000012-pd20231102-1525-03',
    'log000007-pd20231103-1032-02',
    'log000012-pd20231103-1032-28',
    'log000004-pd20231103-1032-43'
]

# SG 필터의 매개변수
window_size = [5, 7, 9, 11, 13]
polynomial_order = [2]  # 다항식의 차수

# 파일마다 스무딩을 진행하기 위해
for file_name in file_name_list:
    # 엑셀 파일 경로
    txt_file = file_path + file_name +'.txt'

    # txt 파일에서 데이터 읽어와서 판다스 데이터프레임으로 변환
    df_origin = pd.read_csv(txt_file, sep='\t', index_col=None)

    # # Cycle이 6 이후인 데이터만 선택, 초반 spike를 무시하기 위해
    # df_origin = df_origin[df_origin['Cycle'] > 5]

    col_num = df_origin.shape[1]     # well 개수를 저장하는 리스트
    col_head = df_origin.columns     # 데이터의 열 제목을 저장하는 리스트

    print("열제목 : ",col_head)
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
    # # 엑셀 파일에 데이터 작성
    # with pd.ExcelWriter(save_path + file_name + '.xlsx') as writer:
    #     df_origin.to_excel(writer, sheet_name='origin'.
    #                        format(window_size[i], polynomial_order[j]), index=False)
    #     for i in range(len(window_size)):
    #         for j in range(len(polynomial_order)):
    #             df_FSmoothing[i][j].to_excel(writer, sheet_name='Sheet_{}_{}'.
    #                                          format(window_size[i], polynomial_order[j]), index=False)
    # ================================================ 수정 중인 부분 ================================================
    # 2행 3열의 서브플롯을 생성하고, 각 서브플롯의 크기를 (10, 10)으로 설정합니다.
    fig, axes = plt.subplots(2, 3, figsize=(10, 10), sharex=False)

    cnt = 0
    # 서브플롯의 행에 대한 반복문
    for j in range(2):
        # 서브플롯의 열에 대한 반복문
        for k in range(3):
            # 첫 번째 서브플롯에는 원본 데이터를 그립니다.
            if j == 0 and k == 0:
                # 'col_head'에 있는 각 열에 대해
                for index in col_head[2:]:
                    # CT 값을 감지합니다.
                    print('file_name :', f'{file_name}')
                    CT_x, CT_y = detect_CT(df_origin[index])
                    # 원본 데이터를 그립니다.
                    axes[j, k].plot(df_origin[col_head[0]][:-5], df_origin[index][5:], label=str(index))
                    print("바꾸기 전 길이 : ", len(df_origin[col_head[0]]), len(df_origin[index]))
                    print("바꾸고 난 후 길이 : ", len(df_origin[col_head[0]][:-5]), len(df_origin[index][5:]))

                    # CT 값이 10과 44 사이에 있다면, 해당 점을 그립니다.
                    if 10 < CT_x < 44:
                        print(f"{index} ({file_name}): {CT_x}, {CT_y}")
                        axes[j, k].scatter(CT_x, CT_y, c='red', label=f'{index} : {CT_x}')
                # 서브플롯의 제목을 설정합니다.
                axes[j, k].set_title(str(file_name))
                # 범례를 추가합니다.
                axes[j, k].legend()
            # 나머지 서브플롯에는 스무딩된 데이터를 그립니다.
            else:
                # 'col_head'에 있는 각 열에 대해
                for index in col_head[2:]:
                    # 스무딩된 데이터를 그립니다.
                    axes[j, k].plot(df_origin[col_head[0]][:-5], df_FSmoothing[cnt][0][index][5:], label=str(index))
                # 서브플롯의 제목을 설정합니다.
                axes[j, k].set_title('Window Size : ' + str(window_size[cnt]))
                cnt += 1
            # 범례를 추가합니다.
            axes[j, k].legend()
            # x축 레이블을 설정합니다.
            axes[j, k].set_xlabel("Cycle")
            # 그리드를 추가합니다.
            axes[j, k].grid(True)
    # 그래프를 출력합니다.
    plt.show()

    # plt.savefig(f'C:/Users/KimHyeongJun/Desktop/바이오메듀스/데이터/LabG CTNG 결과/smoothing/MemoryLength 변화/고농도/{file_name}.png')
    # ================================================ 수정 중인 부분 ================================================





