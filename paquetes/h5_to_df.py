import pandas as pd
import h5py
import numpy as np

def h5_to_digihits(file):
    # open h5 file and get data for test events
    data_path = file
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

    dict_hits = {'eventid': np.array([id for sublist in l_eventid for id in sublist]),
                 'charge':  np.array([chg for sublist in l_charge for chg in sublist]),
                 'time':    np.array([time for sublist in l_time for time in sublist]),
                 'pmtid':   np.array([pmtid for sublist in l_pmtid for pmtid in sublist]),
                 'label':   np.array([label for sublist in l_label for label in sublist])}

    df = pd.DataFrame.from_dict(dict_hits)

    df_geo = pd.read_csv('/Users/diiego/software/wcsim_replacement/build/geofile_NuPRISMBeamTest_16cShort_mPMT.csv')

    x = [df_geo[df_geo['mPMTID'] == i+1]['X'].values[0] for i in df['pmtid']]
    y = [df_geo[df_geo['mPMTID'] == i+1]['Y'].values[0] for i in df['pmtid']]
    z = [df_geo[df_geo['mPMTID'] == i+1]['Z'].values[0] for i in df['pmtid']]

    #for i in df['pmtid']:
    #    x.append(df_geo[df_geo['mPMTID'] == i+1]['X'].values[0])
    #    y.append(df_geo[df_geo['mPMTID'] == i+1]['Y'].values[0])
    #    z.append(df_geo[df_geo['mPMTID'] == i+1]['Z'].values[0])

    df['X'] = x
    df['Y'] = y
    df['Z'] = z
    df['R'] = [np.sqrt(i**2 + j**2 + k**2) for i,j,k in zip(x,y,z)]

    return df
