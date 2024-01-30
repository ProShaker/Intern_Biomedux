from def_AdaptiveSGfilter import *


file_path = 'C:/Users/KimHyeongJun/Desktop/바이오메듀스/데이터/원본 데이터/LabG CTNG 결과/SCL 임상검체/'

# 그 파일에서 txt 파일만 배열로 생성
file_list = [f for f in os.listdir(file_path) if f.endswith('.txt') and 'pd' in f]

for file_name in file_list:
    temp_path = os.path.join(file_path, file_name)

    # txt 파일에서 데이터 읽어와서 판다스 데이터프레임으로 변환
    df_origin = pd.read_csv(temp_path, sep='\t', index_col=None)
    #
    # # Cycle이 6 이후인 데이터만 선택, 초반 spike를 무시하기 위해
    # df_origin = df_origin[df_origin['Cycle'] > 5]

    col_head = df_origin.columns  # 데이터의 열 제목을 저장하는 리스트

    # 인덱스가 2 이상인 열만 선택
    df_origin = df_origin[col_head[2:]]

    # DataFrame을 Excel 파일로 저장
    excel_file_name = file_name.replace('.txt', '.xlsx')  # 파일명 변경
    excel_file_path = os.path.join(file_path, excel_file_name)  # 저장할 파일 경로
    df_origin.to_excel(excel_file_path, index=False)  # Excel 파일로 저장

