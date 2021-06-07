import os
import numpy as np
import mne 
import matplotlib
from mne.preprocessing import (ICA, create_eog_epochs, create_ecg_epochs,
                               corrmap)

## Load all relevant EEG data
def eeg_data_loader():
    eeg_datapath = r"C:\Users\kaiyu\Lab Work\TestLearning\EEG Data"
    ##load data path
    raw_eeg_data = {}
    for root, dirs, files in os.walk(eeg_datapath):
        for f in files: 
            if ".vhdr" in f:
                print("vhdr found")
                eeg_raw_file = os.path.join(root, f)
                raw =  mne.io.read_raw_brainvision(eeg_raw_file)
                raw.crop(tmax=100)
                raw_eeg_data[f] = raw
    return raw_eeg_data

## plot the raw EEG data
def eeg_raw_plotter(raw_eeg):
    raw_eeg.plot_psd(fmax=50)
    raw_eeg.plot(duration=5, n_channels=30, block=True)

## artifact detection based on https://mne.tools/stable/auto_tutorials/preprocessing/40_artifact_correction_ica.html#tut-artifact-ica
def eeg_artifact_detection(raw_eeg):
    eog_evoked = create_eog_epochs(raw_eeg).average()
    eog_evoked.apply_baseline(baseline=(None, -0.2))
    eog_evoked.plot_joint()

def eeg_heartbeat_detection(raw_eeg):
    ecg_evoked = create_ecg_epochs(raw_eeg).average()
    ecg_evoked.apply_baseline(baseline=(None, -0.2))
    ecg_evoked.plot_joint()

def ica_processing(raw_eeg):
    filtered_raw = raw_eeg.copy()
    filtered_raw.load_data().filter(l_freq=1., h_freq=None)
    ica = ICA(n_components=15, max_iter='auto')
    ica.fit(filtered_raw)
    raw_eeg.load_data()
    ica.plot_sources(raw_eeg, block=True)

data = eeg_data_loader()
for key in data.keys():
    ica_processing(data[key])
    
    



