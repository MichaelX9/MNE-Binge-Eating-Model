import os
import numpy as np
import mne 
import matplotlib
# matplotlib.use('TkAgg')

## loading data and checking loaded info
sample_data_folder = mne.datasets.sample.data_path()
print(sample_data_folder)
print(mne.datasets.sample)
sample_data_raw_file = os.path.join(sample_data_folder, 'MEG', 'sample', 'sample_audvis_filt-0-40_raw.fif')
raw = mne.io.read_raw_fif(sample_data_raw_file)
print(raw)
print(raw.info)

## base plotting functions for Raw objects
raw.plot_psd(fmax=50)
raw.plot(duration=5, n_channels=30)

#Pre-processing with ICA
ica = mne.preprocessing.ICA(n_components=20, random_state=97, max_iter=800)
ica.fit(raw)

##Choosing removal components 
ica.exclude = [1,2]
ica.plot_properties(raw, picks=ica.exclude)

##Apply the ICA preprocessing and compare with raw original data
orig_raw = raw.copy() 
raw.load_data()
ica.apply(raw) 

##Choose channels for display to show products of ICA processing
chs = ['MEG 0111', 'MEG 0121', 'MEG 0131', 'MEG 0211', 'MEG 0221', 'MEG 0231',
       'MEG 0311', 'MEG 0321', 'MEG 0331', 'MEG 1511', 'MEG 1521', 'MEG 1531',
       'EEG 001', 'EEG 002', 'EEG 003', 'EEG 004', 'EEG 005', 'EEG 006',
       'EEG 007', 'EEG 008']
chan_idxs = [raw.ch_names.index(ch) for ch in chs]
orig_raw.plot(order=chan_idxs, start=12, duration=4)
raw.plot(order=chan_idxs, start=12, duration=4, block=True)

