#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 11 11:32:32 2023

@author: diiego
"""

import pandas as pd
import h5py
import numpy as np

dh = h5py.File('/Users/diiego/software/wcsim_replacement/build/h5/wcsim_1000neutrons_1to10MeV_DR14000_QESD_BGO_Threshold10_PrePos1s.h5', 'r')

# open h5 file and get data for test events
data_path = "/Users/diiego/software/wcsim_replacement/build/h5/wcsim_1000neutrons_1to10MeV_DR14000_QESD_BGO_Threshold3_PrePos1s.h5"
h5_file = h5py.File(data_path, "r")

test_idxs = np.linspace(0,
                        len(h5_file['event_hits_index'][:])-1,
                        len(h5_file['event_hits_index'][:]), 
                        dtype=int)

h5_angles     = np.array(h5_file['angles'])[test_idxs].squeeze()
h5_energies   = np.array(h5_file['energies'])[test_idxs].squeeze()
h5_positions  = np.array(h5_file['positions'])[test_idxs].squeeze()
h5_labels     = np.array(h5_file['labels'])[test_idxs].squeeze()
h5_root_files = np.array(h5_file['root_files'])[test_idxs].squeeze()
h5_event_ids  = np.array(h5_file['event_ids'])[test_idxs].squeeze()
h5_vetos      = np.array(h5_file['veto'])[test_idxs].squeeze()
events_hits_index = np.append(h5_file['event_hits_index'], h5_file['hit_pmt'].shape[0])
h5_hits_start = events_hits_index[test_idxs].squeeze()
h5_hits_end   = events_hits_index[test_idxs+1].squeeze()
h5_nhits      = h5_hits_end - h5_hits_start

# Create the hits dataframe

# Get charge and timing information for all events.
h5_all_hit_charge = np.array(h5_file['hit_charge'])
h5_all_hit_time   = np.array(h5_file['hit_time'])
h5_all_hit_pmt    = np.array(h5_file['hit_pmt'])

# # Set the event ID, particle ID, and event type.
nhits = len(h5_all_hit_pmt)
l_charge, l_time, l_pmtid, l_eventid, l_label = [],[],[],[],[]
for id,nh,label,istart,iend in zip(h5_event_ids,h5_nhits,h5_labels,h5_hits_start,h5_hits_end):
  subarr_charge  = h5_all_hit_charge[istart:iend]
  subarr_time    = h5_all_hit_time[istart:iend]
  subarr_pmtid   = h5_all_hit_pmt[istart:iend]
  subarr_eventid = np.ones(nh)*id
  subarr_label   = np.ones(nh)*label

  #print("Event",id,"with hits",nh,"start",istart,"and end",iend)
  l_charge.append(subarr_charge)
  l_time.append(subarr_time)
  l_pmtid.append(subarr_pmtid)
  l_eventid.append(subarr_eventid)
  l_label.append(subarr_label)

dict_hits = {'charge':  np.array([chg for sublist in l_charge for chg in sublist]),
              'time':    np.array([time for sublist in l_time for time in sublist]),
              'pmtid':   np.array([pmtid for sublist in l_pmtid for pmtid in sublist]),
              'eventid': np.array([id for sublist in l_eventid for id in sublist]),
              'label':   np.array([label for sublist in l_label for label in sublist])}

df_hits = pd.DataFrame.from_dict(dict_hits)