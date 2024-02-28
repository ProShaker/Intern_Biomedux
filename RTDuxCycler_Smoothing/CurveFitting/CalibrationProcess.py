# 보정 데이터프레임을 더해주는 코드


import pandas as pd
import os
import numpy as np

# 보정값 파일
Calibration_path = r"C:\Users\KimHyeongJun\Desktop\바이오메듀스\데이터\RTDuxCycler_WellCalibration\CalibrationData.xlsx"
# 보정값 파일을 읽어옵니다
calibration_df = pd.read_excel(Calibration_path)
# 보정값 데이터프레임의 필요한 부분만 추출합니다 (B2:Z60)
calibration_df = calibration_df.iloc[1:, 1:]

# 엑셀 파일이 저장된 폴더
folder_path = r"C:\Users\KimHyeongJun\Desktop\바이오메듀스\데이터\원본 데이터\Calibration\보정 후(6cycle부터 스무딩)\농도별\1e5"
# 폴더 내의 모든 엑셀 파일을 읽어옵니다
file_name_list = [f for f in os.listdir(folder_path) if f.endswith(('.xls', '.xlsx')) if f.startswith('smoothing')]
save_path = r"C:\Users\KimHyeongJun\Desktop\바이오메듀스\데이터\RTDuxcycler_WellCalibration\보정 후\LowLightCompensation\1e5\\"

# 각 엑셀 파일에 대해
for file_name in file_name_list:
    # 파일 경로를 만듭니다
    file_path = os.path.join(folder_path, file_name)

    # 엑셀 파일을 읽어옵니다
    df = pd.read_excel(file_path)
    # 원본 데이터와 보정 데이터프레임을 더해준다.
    df_corrected = df.iloc[1:61, 1:26].add(calibration_df.values)

    # 보정된 데이터프레임을 새 엑셀 파일로 저장합니다
    df_corrected.to_excel(save_path + 'calibrated_' + file_name, index=False, header=True)

