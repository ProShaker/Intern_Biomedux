from def_AdaptiveSGfilter import *

# 스무딩할 파일 저장된 경로
file_path = 'C:/Users/KimHyeongJun/Desktop/바이오메듀스/데이터/LabG CTNG 결과/저농도/'
# 스무딩한 파일을 저장할 경로
save_path = 'C:/Users/KimHyeongJun/Desktop/바이오메듀스/데이터/LabG CTNG 결과/smoothing/20이상/저농도'

# 스무딩할 txt 파일의 이름 리스트
file_name_list = [
    'log000004-pd20231109-1017-33',
    'log000013-pd20231110-1108-00',
    'log000009-pd20231110-1107-49',
    'log000004-pd20231110-1108-22',
    'log000004-pd20231114-1034-01',
    'log000007-pd20231114-1504-41',
    'log000009-pd20231114-1504-48'
]

# SG 필터의 매개변수
window_size = [5, 7, 9, 11, 13]
polynomial_order = [2]

# 각 파일마다 스무딩을 수행하기 위한 반복문
for file_name in file_name_list:

    # txt 파일경로
    txt_file = file_path + file_name +'.txt'

    # txt 파일에서 데이터 읽어와서 판다스 데이터프레임으로 변환
    df_origin = pd.read_csv(txt_file, sep='\t', index_col=None)

    # 초반 spike를 무시하기 위해 Cycle이 6 이후인 데이터만 선택
    df_origin = df_origin[df_origin['Cycle'] > 5]
    print(df_origin)
    col_num = df_origin.shape[1]     # well 개수를 저장하는 리스트
    col_head = df_origin.columns     # 데이터의 열 제목을 저장하는 리스트

    # 필터링된 데이터를 저장하기 위한 리스트 선언
    # Column 별로 데이터를 저장하기 위해 2차원 리스트 선언
    C_y1 = [[] for _ in range(col_num)]

    # SG필터링을 적용한 데이터를 위한 리스트
    # 매개변수 별로 데이터를 저장하기 위해 4차원 리스트 선언
    C_y1_filtered = [[copy.deepcopy(C_y1) for _ in range(len(polynomial_order))] for _ in range(len(window_size))]

    # SG필터링을 적용한 데이터에 대해 판다스 데이터 프레임 꼴로 저장할 리스트
    df_FSmoothing = [[copy.deepcopy(C_y1) for _ in range(len(polynomial_order))] for _ in range(len(window_size))]

    # 각 well의 데이터(엑셀 파일)를 2차원 리스트에 저장
    for i, column in enumerate(col_head):
        C_y1[i] = df_origin[column].values.tolist()

    # 각 열에 대해 매개변수를 바꿔주며 SG 필터 적용
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
    #     df_origin.to_excel(writer,sheet_name='origin'.
    #                        format(window_size[i], polynomial_order[j]),index=False)
    #     for i in range(len(window_size)):
    #         for j in range(len(polynomial_order)):
    #             df_FSmoothing[i][j].to_excel(writer,sheet_name='Sheet_{}_{}'.
    #                                          format(window_size[i], polynomial_order[j]),index=False)

    # ================================================ 수정 중인 부분 ================================================
    fig, axes = plt.subplots(2, 3, figsize=(10, 10), sharex=False)
    cnt = 0
    # subplot의 행 반복문
    for j in range(2):
        # subplot의 열 반복문
        for k in range(3):
            # 원본은 0, 0에 plot
            if j == 0 and k == 0:
                for index in col_head[2:]:
                    axes[j, k].plot(df_origin[col_head[0]], df_origin[index], label=str(index))
                axes[j, k].set_title(str(file_name))
                axes[j, k].legend()  # 범례 추가
            # 나머지 데이터는 행, 열을 바꿔가며 스무딩한 데이터 출력
            else:
                # 열 데이터를 plot에 추가하기 위한 반복문
                for index in col_head[2:]:
                    axes[j, k].plot(df_origin[col_head[0]], df_FSmoothing[cnt][0][index], label=str(index))
                axes[j, k].set_title('Window Size : ' + str(window_size[cnt]))
                cnt += 1
            axes[j, k].legend()  # 범례 추가
            axes[j, k].set_xlabel("Cycle")
            axes[j, k].grid(True)
    # plt.show()
    plt.savefig(f'C:/Users/KimHyeongJun/Desktop/바이오메듀스/데이터/LabG CTNG 결과/smoothing/MemoryLength 변화/저농도/{file_name}.png')
    # # 기울기 변화가 가장 큰 부분 표시
    # max_slope_index = np.argmax(df_origin[col_head[0]].diff().diff())
    # max_slope_cycle = df_origin.index[max_slope_index + 2]
    # max_slope_value = df_origin[col_head[0]][max_slope_index + 2]
    # axes[0, 0].annotate('Max Slope', xy=(max_slope_cycle, max_slope_value),
    #                     xytext=(max_slope_cycle, max_slope_value + 10),
    #                     arrowprops=dict(facecolor='black', arrowstyle='->'),
    #                     fontsize=10, ha='center')
    # ================================================ 수정 중인 부분 ================================================