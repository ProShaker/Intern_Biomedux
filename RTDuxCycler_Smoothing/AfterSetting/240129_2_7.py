from def_AdaptiveSGfilter import *

file_path = 'C:/Users/KimHyeongJun/Desktop/바이오메듀스/데이터/원본 데이터/240129/'
save_path = 'C:/Users/KimHyeongJun/Desktop/바이오메듀스/데이터/LabG CTNG 결과/smoothing/fixed_2_7/240129/'

# 그 파일에서 txt 파일만 배열로 생성
file_name_list = [f for f in os.listdir(file_path) if f.endswith('.txt') and 'pd' in f]

# SG 필터의 매개변수
window_size = 7
polynomial_order = 2  # 다항식의 차수

for file_name in file_name_list:
    # 엑셀 파일 경로
    txt_file = file_path + file_name

    # txt 파일에서 데이터 읽어와서 판다스 데이터프레임으로 변환
    df_origin = pd.read_csv(txt_file, sep='\t', index_col=None)

    # 데이터의 열 제목을 저장하는 리스트
    col_heads = df_origin.columns

    # 데이터프레임의 복사본을 만듭니다.
    df_filtered = df_origin.copy()

    # 복사본의 각 열에 대해 SG 필터 적용
    for col_head in col_heads[2:]:
        df_filtered[col_head] = savgol_filter(df_filtered[col_head], window_size, polynomial_order)

    print(df_filtered)
    # # 엑셀 파일에 데이터 작성
    # with pd.ExcelWriter(save_path + file_name + '.xlsx') as writer:
    #     df_origin.to_excel(writer, sheet_name='origin'.
    #                        format(window_size[i], polynomial_order[j]), index=False)
    #     for i in range(len(window_size)):
    #         for j in range(len(polynomial_order)):
    #             df_FSmoothing[i][j].to_excel(writer, sheet_name='Sheet_{}_{}'.
    #                                          format(window_size[i], polynomial_order[j]), index=False)
    # # ================================================ 수정 중인 부분 ================================================
    # 1행 2열의 서브플롯을 생성하고, 각 서브플롯의 크기를 (10, 5)로 설정
    fig, axes = plt.subplots(1, 2, figsize=(10, 5), sharex=True, sharey=True)

    # 원본 데이터를 그립니다.
    for col_head in col_heads[2:]:
        # CT 값을 감지합니다.
        CT_x, CT_y = detect_CT(df_origin[col_head])
        # 원본 데이터를 그립니다.
        axes[0].plot(df_origin[col_heads[0]][5:], df_origin[col_head][5:], label=str(col_head))
        axes[0].scatter(CT_x, CT_y, c='red', label=f'{col_head} : {CT_x}')

    axes[0].set_title(str(file_name))
    axes[0].legend()
    axes[0].set_xlabel("Cycle")
    axes[0].grid(True)

    # 스무딩된 데이터를 그립니다.
    for col_head in col_heads[2:]:
        CT_x, CT_y = detect_CT(df_origin[col_head])
        axes[1].plot(df_origin[col_heads[0]][5:], df_filtered[col_head][5:], label=str(col_head))
        axes[1].scatter(CT_x, CT_y, c='red', label=f'{col_head} : {CT_x}')


    axes[1].set_title('Window Size : ' + str(window_size))
    axes[1].legend()
    axes[1].set_xlabel("Cycle")
    axes[1].grid(True)

    # plt.show()
    plt.savefig(save_path + f'{file_name}.png')
    # # ================================================ 수정 중인 부분 ================================================





