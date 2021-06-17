import pandas as pd 
import os 
import shutil

def qualifying_patient_ids(csv_patient_file):
    patient_ids = {'BED': [], 'Non-BED': []}
    df = pd.read_csv(csv_patient_file)
    total_count = 0
    for row in df.itertuples():
        if row.FEV_STOER <= 2:
            patient_ids['Non-BED'].append(row.ID)
        elif row.FEV_STOER >= 8:
            patient_ids['BED'].append(row.ID)
    return patient_ids

def file_collection(eeg_folder, filtered_ids):
    non_BED = r"C:\Users\kaiyu\Lab Work\Sorted Data\Non-BED"
    BED = r"C:\Users\kaiyu\Lab Work\Sorted Data\BED"
    ##load data path
    for root, dirs, files in os.walk(eeg_folder):
        for f in files: 
            file_id = f.split("_")[0]
            if file_id in filtered_ids["Non-BED"]:
                if not os.path.isdir(os.path.join(non_BED, file_id)):
                   os.mkdir(os.path.join(non_BED, file_id))  
                shutil.move(os.path.join(root, f), os.path.join(non_BED, file_id))
            elif file_id in filtered_ids["BED"]:
                if not os.path.isdir(os.path.join(BED, file_id)):
                   os.mkdir(os.path.join(BED, file_id))  
                shutil.move(os.path.join(root, f), os.path.join(BED, file_id))

csv_patient_file = r"C:\Users\kaiyu\Lab Work\FEV.csv"
eeg_folder = r"C:\Users\kaiyu\Lab Work\Lab Data"
filtered_ids = qualifying_patient_ids(csv_patient_file)
file_collection(eeg_folder, filtered_ids)
