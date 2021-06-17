import os
import numpy as np
import mne 
import matplotlib
import matplotlib.pyplot as plt 
from mne.time_frequency import tfr_morlet, psd_multitaper, psd_welch

bed_eeg_datapath = r"C:\Users\kaiyu\Lab Work\Sorted Data\BED"
non_bed_eeg_datapath = r"C:\Users\kaiyu\Lab Work\Sorted Data\Non-BED"

## Load all relevant EEG data
def eeg_data_loader(eeg_datapath):
    ##load data path
    raw_eeg_data = {}
    for root, dirs, files in os.walk(eeg_datapath):
        for d in dirs:
            for f in os.listdir(os.path.join(root, d)): 
                if ".set" in f:
                    eeg_raw_file = os.path.join(root, d, f)
                    raw =  mne.io.read_raw_eeglab(eeg_raw_file)
                    # raw.crop(tmax=100)
                    raw_eeg_data[f] = raw
    return raw_eeg_data

## plot the raw EEG data
def eeg_raw_plotter(raw_eeg):
    # raw_eeg.plot_psd(fmax=50, dB=True, estimate='power')
    # raw_eeg.plot(duration=5, n_channels=30, block=True)
    psd_welch_mean, freq_mean = psd_welch(raw_eeg, average='mean', fmax=50, fmin=0.5, n_fft=1024)
    return psd_welch_mean, freq_mean
    

def raw_epoch_construct(raw_eeg):
    events = mne.events_from_annotations(raw_eeg)
    # events = mne.find_events(raw_eeg)
    picks = mne.pick_types(raw_eeg.info, meg=False, eeg=False, eog=False, stim=False)
    epochs = mne.Epochs(raw_eeg, events[0], preload=True, event_repeated='drop')
    epochs.resample(200, npad='auto')
    return epochs 

def freq_analysis(epochs):
    epochs.plot_psd(average = True)

def relevant_freq_averages(freq_mean):
    relevant_indexes = {"4.5": [], "5": [], "5.5":[]}
    for i in range(len(freq_mean)):
        if 4.5 <= freq_mean[i] < 5:
            relevant_indexes["4.5"].append(i)
        elif 5 <= freq_mean[i] < 5.5:
            relevant_indexes["5"].append(i)
        elif 5.5 <= freq_mean[i] <= 6: 
            relevant_indexes["5.5"].append(i)
    return relevant_indexes
        
def sample_averages(welch_mean, relevant_indexes):
    selected_means = {"4.5": [], "5": [], "5.5": []}
    for ch in welch_mean:
        for i in relevant_indexes["4.5"]:
            selected_means["4.5"].append(ch[i])
        for i in relevant_indexes["5"]:
            selected_means["5"].append(ch[i])
        for i in relevant_indexes["5.5"]:
            selected_means["5.5"].append(ch[i])
    return selected_means

print("code active")
bed_data = eeg_data_loader(bed_eeg_datapath)
non_bed_data = eeg_data_loader(non_bed_eeg_datapath)
bed_averages = {"4.5": [], "5": [], "5.5": []}
non_bed_averages = {"4.5": [], "5": [], "5.5": []}
for key in bed_data.keys():
    bed_welch_mean, bed_freq_mean = eeg_raw_plotter(bed_data[key])
    relevant_indexes = relevant_freq_averages(bed_freq_mean)
    collected_means = sample_averages(bed_welch_mean, relevant_indexes)
    bed_averages["4.5"] += collected_means["4.5"]
    bed_averages["5"] += collected_means["5"]
    bed_averages["5.5"] += collected_means["5.5"]
for key in bed_averages.keys():
    bed_averages[key] = np.asarray(bed_averages[key])
for key in non_bed_data.keys():
    non_bed_welch_mean, non_bed_freq_mean = eeg_raw_plotter(non_bed_data[key])
    relevant_indexes = relevant_freq_averages(non_bed_freq_mean)
    collected_means = sample_averages(non_bed_welch_mean, relevant_indexes)
    non_bed_averages["4.5"] += collected_means["4.5"]
    non_bed_averages["5"] += collected_means["5"]
    non_bed_averages["5.5"] += collected_means["5.5"]
for key in non_bed_averages.keys():
    non_bed_averages[key] = np.asarray(non_bed_averages[key])
bed_average = {"4.5": np.mean(bed_averages["4.5"]), "5": np.mean(bed_averages["5"]), "5.5": np.mean(bed_averages["5.5"])}
non_bed_average = {"4.5": np.mean(non_bed_averages["4.5"]), "5": np.mean(non_bed_averages["5"]), "5.5": np.mean(non_bed_averages["5.5"])}
print(bed_average)
print(non_bed_average)

    
    



