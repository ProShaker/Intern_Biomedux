import pandas as pd
import os

# 보정값 파일
Calibration_path = r"C:\Users\KimHyeongJun\Desktop\바이오메듀스\데이터\RTDuxCycler_WellCalibration\CalibrationData.xlsx"
# 보정값 파일을 읽어옵니다
calibration_df = pd.read_excel(Calibration_path, index_col=None, header=None)
# 보정값 데이터프레임의 필요한 부분만 추출합니다 (B2:Z61)
calibration_df = calibration_df.iloc[1:61, 1:26]

# 엑셀 파일이 저장된 폴더
folder_path = r"C:\Users\KimHyeongJun\Desktop\바이오메듀스\데이터\원본 데이터\Calibration\보정 전\농도별\1e5"
# 폴더 내의 모든 엑셀 파일을 읽어옵니다
file_list = os.listdir(folder_path)

# 각 엑셀 파일에 대해
for file_name in file_list:
    # 파일 경로를 만듭니다
    file_path = os.path.join(folder_path, file_name)

    # 엑셀 파일을 읽어옵니다 (첫 번째 열을 제외)
    df = pd.read_excel(file_path, index_col=None, header=None)

    # 필요한 부분만 추출합니다 (B2:Z61)
    df = df.iloc[1:61, 1:26]

    # 각 셀에 보정값을 더합니다
    df_corrected = df.add(calibration_df)

    # 보정된 데이터프레임을 새 엑셀 파일로 저장합니다
    df_corrected.to_excel(file_path.replace('.xlsx', '_corrected.xlsx'), index=False, header=False)


