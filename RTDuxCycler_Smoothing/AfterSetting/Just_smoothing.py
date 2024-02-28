# smoothing 해주는 코드
# cycle열, 1~5행 제외하고 smoothing 해줌

from def_AdaptiveSGfilter import *

folder_path = 'C:/Users/KimHyeongJun/Desktop/바이오메듀스/데이터/원본 데이터/Calibration/보정 전/농도별/1e5/'
save_path = 'C:/Users/KimHyeongJun/Desktop/바이오메듀스/데이터/원본 데이터/Calibration/보정 후(6cycle부터 스무딩)/농도별/1e5/'

file_name_list = [f for f in os.listdir(folder_path) if f.endswith(('.xls', '.xlsx'))]

# SG 필터의 매개변수
window_size = 7
polynomial_order = 2  # 다항식의 차수

for file_name in file_name_list:
    # 엑셀 파일 경로
    file = folder_path + file_name

    df_origin = pd.read_excel(file)

    # 데이터의 열 제목을 저장하는 리스트
    col_heads = df_origin.columns

    # DataFrame의 크기를 가져와서 같은 크기의 DataFrame을 만듭니다.
    num_rows, num_cols = df_origin.shape
    df_filtered = pd.DataFrame(index=df_origin.index[:-5], columns=df_origin.columns)

    # 복사본의 각 열에 대해 SG 필터 적용
    for idx,col_head in enumerate(col_heads):
        if idx == 0:
            df_filtered[col_head] = df_origin[col_head] + 1
        else:
            df_filtered[col_head] = savgol_filter(df_origin[col_head][5:], window_size, polynomial_order)

    # 엑셀 파일에 데이터 작성
    with pd.ExcelWriter(save_path + 'smoothing_' + file_name) as writer:  # 'smoothing_' 추가
        df_filtered.to_excel(writer, sheet_name='filtered', index=False)
