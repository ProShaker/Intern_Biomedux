import pandas as pd
import os

# 엑셀 파일이 저장된 폴더
folder_path = 'C:/Users/KimHyeongJun/Desktop/바이오메듀스/데이터/원본 데이터/Calibration/보정 후(6cycle부터 스무딩)/'

# 폴더 내의 모든 엑셀 파일을 읽어옵니다
file_name_list = [f for f in os.listdir(folder_path) if f.endswith(('.xls', '.xlsx'))]

# 각 행 인덱스별로 데이터프레임을 저장할 딕셔너리를 만듭니다
df_dict = {}

# 평균을 저장할 빈 데이터프레임을 생성합니다.
averages_df = pd.DataFrame()

# 각 엑셀 파일에 대해
for file_name in file_name_list:
    # 파일 경로를 만듭니다
    file_path = os.path.join(folder_path, file_name)

    # 엑셀 파일을 읽어옵니다 (첫 번째 열을 제외)
    df = pd.read_excel(file_path).iloc[:, 1:]

    # 각 행 인덱스에 대해
    for idx, row in df.iterrows():
        # 해당 인덱스의 데이터프레임이 딕셔너리에 없다면 새로 만듭니다
        if idx not in df_dict:
            df_dict[idx] = []

        # 해당 인덱스의 데이터프레임에 행을 추가합니다
        df_dict[idx].append(row)

# 행 인덱스별로 데이터프레임을 생성합니다
for idx in df_dict:
    df_dict[idx] = pd.concat(df_dict[idx], axis=1).T

    # 최대값을 찾습니다
    max_value = df_dict[idx].max(axis=1)

    # 최대값을 뺍니다
    df_dict[idx] = df_dict[idx].sub(max_value, axis=0)
#
# # 결과를 확인합니다
# for idx, df in df_dict.items():
#     print(f"Cycle: {idx}")
#     print(df)

# 각 데이터프레임에 대해
for idx in df_dict:
    column_averages = df_dict[idx].mean()

    column_averages = column_averages.to_frame().transpose()

    # 계산된 평균을 새로운 데이터프레임에 추가합니다
    averages_df = pd.concat([averages_df, column_averages], ignore_index=True)

# Cycle 열 추가
averages_df.insert(0, 'Cycle', range(len(averages_df)))

# 모든 값을 양수로 바꿉니다
averages_df = averages_df.abs()

# 결과를 출력합니다
print(averages_df)

# 엑셀 파일로 저장합니다
output_path = r"C:\Users\KimHyeongJun\Desktop\바이오메듀스\데이터\원본 데이터\Calibration\CalibrationData.xlsx"
averages_df.to_excel(output_path, index=False)
print(f"엑셀 파일이 {output_path}에 저장되었습니다.")

