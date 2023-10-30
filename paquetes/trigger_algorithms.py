#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 12:47:19 2023

@author: diiego
"""

import numpy             as np
import pandas            as pd
import matplotlib.pyplot as plt

def gamma_trigger(triggerWindow=200, hitThreshold=6):
    count         = []
    trigger_times = []
    dataFrame     = pd.read_csv("~/Desktop/df_trueHits_bgo_DRQE")
    
    for event in np.unique(dataFrame['event_id']):
        print("Processing Event {}".format(event))
        
        # Min time is literally min time in event
        min_time = np.min(dataFrame[(dataFrame['event_id'] == event)]['true_hit_time'])
        max_time = min_time + triggerWindow
        print("Initial min_time: {} ns".format(min_time))
        print("Initial max_time: {} ns".format(max_time))
        
        # Loop over all event times using biggest time as upper boundary
        while min_time <= np.max(dataFrame[(dataFrame['event_id'] == event)]['true_hit_time']):
            
            #Threshold condition
            if len(dataFrame[(dataFrame['event_id'] == event) & 
                             (dataFrame['true_hit_time'] >= min_time) & 
                             (dataFrame['true_hit_time'] < max_time)]) >= hitThreshold:
            
                count.append(event)
                print('En el evento {} se activa el trigger con la luz que sale del centelleo'.format(event))
                
                # Save the event and the time in which the trigger is activated
                trigger_times.append([event, min_time])
                break
            
            # Update window
            min_time = max_time
            max_time += triggerWindow
            print("Updated min_time: {} ns".format(min_time))
            print("Updated max_time: {} ns".format(max_time))
    
    print(' ')
    print('There are {} events with light comming from inside BGO in the neutron simulation (i.e. Scintillation light).\n' 
          'In {} of those the trigger is activated with the hits produced by the Scintillation light.\n'
          'This represent {:.2f}% of the total'.format(len(np.unique(dataFrame['event_id'])), 
                                                       len(count), 
                                                       len(count)/len(np.unique(dataFrame['event_id']))*100))
    
    return trigger_times


def neutron_trigger(triggerWindow=10000, hitThreshold=15, gammaWindow=200, gammaThreshold=6):
    outside_bgo_dataFrame = pd.read_csv("~/Desktop/df_trueHits_outside_bgo_DRQE")
    candidateInfo         = pd.DataFrame(columns=['event_id', 'A', 'B', 'C', 'D', 'E'])
    gammaTriggerWindow    = gammaWindow
    gammaHitThreshold     = gammaThreshold
    eventInfo = []
    xfInfo = []
    yfInfo = []
    zfInfo = []
    rfInfo = []
    timeInfo = []
    
    print("NOW RUNNING GAMMA TRIGGER:")
    print("Window width: {}".format(gammaTriggerWindow))
    print("Hit Threshold: {}".format(gammaHitThreshold))
    trigger_times = gamma_trigger(gammaTriggerWindow, gammaHitThreshold)
    print("END OF GAMMA TRIGGER RUN")
    print(" ")
    print("NOW RUNNING NEUTRON TRIGGER")
    
    # Iterate in the event, trigger time list
    for i in trigger_times:
        event = i[0] # Current Event
        print("Processing event {}".format(event))
    
        min_time = i[1] # Initial time is now the time "where" the trigger was activated by the scint light
        max_time = min_time + triggerWindow
        print("Initial min_time: {} ns".format(min_time))
        print("Initial max_time: {} ns".format(max_time))
    
        print("Max time limit is: {:.2f} ns".format(np.max(outside_bgo_dataFrame[outside_bgo_dataFrame['event_id'] == event]['true_hit_time'])))
        
        # Loop using the biggest time in event as upper boundary
        while min_time <= np.max(outside_bgo_dataFrame[outside_bgo_dataFrame['event_id'] == event]['true_hit_time']):
            # Filter the DataFrame: event and time characteristics
            window = outside_bgo_dataFrame[(outside_bgo_dataFrame['event_id'] == event) & 
                             (outside_bgo_dataFrame['true_hit_time'] >= min_time) & 
                             (outside_bgo_dataFrame['true_hit_time'] < max_time)]
            
            # Hits Threshold condition
            if len(window) >= hitThreshold:
                print("Updated min_time: {} ns".format(min_time))
                print("Updated max_time: {} ns".format(max_time))
                print("En esta ventana temporal hay un candidato a neutrón")
                
                # Save candidate info
                tmp_candidateInfo = np.array([event, 
                                              window['hit_x'].values, 
                                              window['hit_y'].values, 
                                              window['hit_z'].values, 
                                              window['true_hit_time'].values], dtype='object')
                
                eventInfo.append(tmp_candidateInfo[0])
                xfInfo.append(tmp_candidateInfo[1])
                yfInfo.append(tmp_candidateInfo[2])
                zfInfo.append(tmp_candidateInfo[3])
                rfInfo.append(np.sqrt(tmp_candidateInfo[1]**2 + tmp_candidateInfo[2]**2 + tmp_candidateInfo[3]**2))
                timeInfo.append(tmp_candidateInfo[4])
            
            # Update window 
            min_time = max_time
            max_time += triggerWindow
            #print("Updated min_time: {} ns".format(min_time))
            #print("Updated max_time: {} ns".format(max_time))
          
    candidateInfo['event'] = eventInfo
    candidateInfo['A'] = xfInfo
    candidateInfo['B'] = yfInfo
    candidateInfo['C'] = zfInfo
    candidateInfo['D'] = rfInfo
    candidateInfo['E'] = timeInfo

    candidateInfo = candidateInfo.explode(list('ABCDE'))
    
    candidateInfo = candidateInfo.rename(columns={'A':'hit_x',
                                              'B':'hit_y',
                                              'C':'hit_z',
                                              'D':'hit_r',
                                              'E':'hit_time'})
            
    return candidateInfo

#candidateInfo = neutron_trigger(30, 7, 200, 6)
#with open(r'/Users/diiego/Library/Mobile\ Documents/com~apple~CloudDocs/Desktop/DIEGO_cloud/USC/PHD/HK/HK\ #SOURCES/code/ambe_source/npz_ana/candidateInfo.txt', 'w') as fp:
#    for item in candidateInfo:
#        fp.write("%s\n" % item)
#    print('Done')
        