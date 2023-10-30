import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)


def truehits_info_to_df(file):
    npz = np.load(file, allow_pickle=True)

    event = npz['event_id']
    hit_parent = npz['true_hit_parent']
    #position = npz['position']
    #direction = npz['direction']
    true_hit_pmt = npz['true_hit_pmt']
    true_hit_time = npz['true_hit_time']
    true_hit_start_time = npz['true_hit_start_time']
    true_hit_pos = npz['true_hit_pos']
    true_hit_start_pos = npz['true_hit_start_pos']

    data = [list((i,
                  thparent,
                  #k[0],
                  #k[1],
                  #k[2],
                  #l[0],
                  #l[1],
                  #l[2],
                  thp,
                  tht,
                  thst,
                  thpos[:, 0],
                  thpos[:, 1],
                  thpos[:, 2],
                  thsp[:, 0],
                  thsp[:, 1],
                  thsp[:, 2])) for i, thparent, thp, tht, thst, thpos, thsp in zip(event,
                                                                                         hit_parent,
                                                                                         #position,
                                                                                         #direction,
                                                                                         true_hit_pmt,
                                                                                         true_hit_time,
                                                                                         true_hit_start_time,
                                                                                         true_hit_pos,
                                                                                         true_hit_start_pos)]

    df = pd.DataFrame(data, columns=['event_id',
                                     'J',
                                     #'xi',
                                     #'yi',
                                     #'zi',
                                     #'dxi',
                                     #'dyi',
                                     #'dzi',
                                     'A',
                                     'B',
                                     'C',
                                     'D',
                                     'E',
                                     'F',
                                     'G',
                                     'H',
                                     'I'])

    df = df.explode(list('JABCDEFGHI'))

    df = df.rename(columns={"A": "true_hit_pmt", "B": "true_hit_time", 'C': 'true_hit_start_time',
                            'D': 'hit_x', 'E': 'hit_y', 'F': 'hit_z',
                            'G': 'hit_start_x', 'H': 'hit_start_y', 'I': 'hit_start_z',
                            'J': 'true_hit_parent'})

    return df


def track_info_to_df(file):
    npz = np.load(file, allow_pickle=True)

    event    = npz['event_id']
    position = npz['position']
    direction = npz['direction']
    track_id = npz['track_id']
    track_pid = npz['track_pid']
    track_parent = npz['track_parent']
    track_creator_process = npz['track_creator_process']
    track_start_time = npz['track_start_time']
    track_energy = npz['track_energy']
    track_start_position = npz['track_start_position']
    track_stop_position = npz['track_stop_position']
    

    data = [list((i,
                  k[0],
                  k[1],
                  k[2],
                  l[0],
                  l[1],
                  l[2],
                  tpi,
                  ti,
                  tp,
                  tcp,
                  tst,
                  te,
                  tsp[:, 0],
                  tsp[:, 1],
                  tsp[:, 2],
                  top[:, 0],
                  top[:, 1],
                  top[:, 2])) for i, k, l, tpi, ti, tp, tcp, tst, te, tsp, top in zip(event,
                                                                         position,
                                                                         direction,
                                                                         track_pid,
                                                                         track_id,
                                                                         track_parent,
                                                                         track_creator_process,
                                                                         track_start_time,
                                                                         track_energy,
                                                                         track_start_position,
                                                                         track_stop_position)]

    df = pd.DataFrame(data, columns=['event_id',
                                     'xi',
                                     'yi',
                                     'zi',
                                     'dxi',
                                     'dyi',
                                     'dzi',
                                     'A',
                                     'J',
                                     'K',
                                     'L',
                                     'B',
                                     'C',
                                     'D',
                                     'E',
                                     'F',
                                     'G',
                                     'H',
                                     'I'])

    df = df.explode(list('AJKLBCDEFGHI'))

    df = df.rename(columns={"A": "track_pid", "J": "track_id", "K":"track_parent", "L":"track_creator_process",
                            "B": "track_ti", 'C': 'track_energy',
                            'D': 'track_xi', 'E': 'track_yi', 'F': 'track_zi',
                            'G': 'track_xf', 'H': 'track_yf', 'I': 'track_zf'})

    return df
