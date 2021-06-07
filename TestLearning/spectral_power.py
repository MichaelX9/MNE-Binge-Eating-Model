import os
import numpy as np
import mne 
import matplotlib
import matplotlib.pyplot as plt 
from mne.time_frequency import tfr_morlet, psd_multitaper, psd_welch

## Load all relevant EEG data
def eeg_data_loader():
    eeg_datapath = r"C:\Users\kaiyu\Lab Work\TestLearning\EEG Preprocessed\sub-032308"
    ##load data path
    raw_eeg_data = {}
    for root, dirs, files in os.walk(eeg_datapath):
        for f in files: 
            if ".set" in f:
                eeg_raw_file = os.path.join(root, f)
                raw =  mne.io.read_raw_eeglab(eeg_raw_file)
                # raw.crop(tmax=100)
                raw_eeg_data[f] = raw
    return raw_eeg_data

## plot the raw EEG data
def eeg_raw_plotter(raw_eeg):
    print(raw_eeg.ch_names)
    raw_eeg.plot_psd(fmax=50)
    raw_eeg.plot(duration=5, n_channels=30, block=True)

def raw_epoch_construct(raw_eeg):
    events = mne.events_from_annotations(raw_eeg)
    # events = mne.find_events(raw_eeg)
    picks = mne.pick_types(raw_eeg.info, meg=False, eeg=False, eog=False, stim=False)
    epochs = mne.Epochs(raw_eeg, events[0], preload=True, event_repeated='drop')
    epochs.resample(200, npad='auto')
    return epochs 

def freq_analysis(epochs):
    epochs.plot_psd(average = True)

data = eeg_data_loader()
for key in data.keys():
    epochs = raw_epoch_construct(data[key])
    freq_analysis(epochs)
    
    



