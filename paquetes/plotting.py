#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 12:38:41 2023

@author: diiego
"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def map_list(lst):
    max_val = np.max(lst)
    min_val = np.min(lst)
    new_lst = []
    for val in lst:
        new_val = ((val - min_val) / (max_val - min_val)) * 55 + 5
        new_lst.append(new_val)
    return new_lst

def plot3d(df, event, title='Generic Title', colormap='jet', mode='time', alpha=0.3):
    x = np.float64(df[(df['event_id'] == event) & (df['hit_r'] > 100)]['hit_x'].values)
    y = np.float64(df[(df['event_id'] == event) & (df['hit_r'] > 100)]['hit_z'].values)
    z = np.float64(df[(df['event_id'] == event) & (df['hit_r'] > 100)]['hit_y'].values)

    t = np.float64(df[(df['event_id'] == event) & (df['hit_r'] > 100)]['true_hit_time'].values)
    r = np.float64(df[(df['event_id'] == event) & (df['hit_r'] > 100)]['hit_start_r'].values)
    norm_r = map_list(r)
    markers = ['*' if ri <= np.sqrt(2**2+2**2) else 'o' for ri in r]
    
    fig = plt.figure()
    ax = plt.axes(projection='3d')

    if mode=='marker':
        for xi,yi,zi,ti,ri,mi in zip(x,y,z,t,norm_r,markers):
            p = ax.scatter3D(xi, yi, zi, c=ti, s=ri, marker=mi, cmap=colormap, alpha=alpha)
       
    elif mode=='time':
        p = ax.scatter3D(x, y, z, c=t, s=map_list(r), cmap=colormap, alpha=alpha)
        
    fig.colorbar(p, ax=ax, label='True Hit Time')

    ax.set_title("{}".format(title))
    ax.set_xlabel('X [mm]');
    ax.set_ylabel('Y [mm]');
    ax.set_zlabel('Z [mm]');
    
    
def plot3d_digihits(df, title='Generic Title', third_variable='hit_time', colormap='jet', alpha=0.3):
    x = np.float64(df['X'].values)
    y = np.float64(df['Z'].values)
    z = np.float64(df['Y'].values)

    t = np.float64(df[third_variable].values)

    fig = plt.figure()
    ax = plt.axes(projection='3d')

    p = ax.scatter3D(x, y, z, c=t, cmap=colormap, alpha=alpha)
    fig.colorbar(p, ax=ax)

    ax.set_title("{}".format(title))
    ax.set_xlabel('X [mm]');
    ax.set_ylabel('Y [mm]');
    ax.set_zlabel('Z [mm]');


def unwrapped_cylinder(df, colormap='jet'):
    fig = plt.figure()
    fig.set_figheight(18.0)
    fig.set_figwidth(21.0)

    # Initial parameters of the cylinder
    r = 168
    x = np.float64(df['hit_x'].values)
    y = np.float64(df['hit_z'].values)
    z = np.float64(df['hit_y'].values)
    t = np.float64(df['true_hit_time'].values)

    # Tranversal projection
    theta = np.arctan2(y, x)
    phi = theta + np.pi
    x_proj = r * phi
    y_proj = z

    # Plot the colobar
    ax_cbar = fig.add_subplot(3, 12, 10)
    matplotlib.colorbar.ColorbarBase(ax_cbar, cmap=colormap,
                                     norm=matplotlib.colors.Normalize(vmin=np.min(t), vmax=np.max(t)))
    ax_cbar.set_title("Time (ns)")

    # Plot the upper lid
    ax1 = fig.add_subplot(3, 3, 2)
    ax1.scatter(x[z > 120], y[z > 120], c=t[z > 120], cmap=colormap)

    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_ylim(-150, 150)
    ax1.set_xlim(-150, 150);

    # Plot the cylinder 'body'
    ax2 = fig.add_subplot(3, 1, 2)
    ax2.scatter(x_proj, y_proj, c=t, cmap=colormap)

    ax2.set_xlabel('X')
    ax2.set_ylabel('Z')
    ax2.set_ylim(-120, 120);

    # Plot the bottom lid
    ax3 = fig.add_subplot(3, 3, 8)
    ax3.scatter(x[z < -120], y[z < -120], c=t[z < -120], cmap=colormap)

    ax3.set_xlabel('X')
    ax3.set_ylabel('Y')
    ax3.set_ylim(-150, 150);
    ax3.set_xlim(-150, 150);

def unwrapped_cylinder_digihits(df, third_variable='hit_time', colormap='jet'):
    fig = plt.figure()
    fig.set_figheight(18.0)
    fig.set_figwidth(21.0)

    # Initial parameters of the cylinder
    r = 168
    x = np.float64(df['X'].values)
    y = np.float64(df['Z'].values)
    z = np.float64(df['Y'].values)
    t = np.float64(df[third_variable].values)

    # Tranversal projection
    theta = np.arctan2(y, x)
    phi = theta + np.pi
    x_proj = r * phi
    y_proj = z

    # Plot the colobar
    ax_cbar = fig.add_subplot(3, 12, 10)
    matplotlib.colorbar.ColorbarBase(ax_cbar, cmap=colormap,
                                     norm=matplotlib.colors.Normalize(vmin=np.min(t), vmax=np.max(t)))
    ax_cbar.set_title("Time (ns)")

    # Plot the upper lid
    ax1 = fig.add_subplot(3, 3, 2)
    ax1.scatter(x[z > 120], y[z > 120], c=t[z > 120], cmap=colormap)

    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_ylim(-150, 150)
    ax1.set_xlim(-150, 150);

    # Plot the cylinder 'body'
    ax2 = fig.add_subplot(3, 1, 2)
    ax2.scatter(x_proj, y_proj, c=t, cmap=colormap)

    ax2.set_xlabel('X')
    ax2.set_ylabel('Z')
    ax2.set_ylim(-120, 120);

    # Plot the bottom lid
    ax3 = fig.add_subplot(3, 3, 8)
    ax3.scatter(x[z < -120], y[z < -120], c=t[z < -120], cmap=colormap)

    ax3.set_xlabel('X')
    ax3.set_ylabel('Y')
    ax3.set_ylim(-150, 150);
    ax3.set_xlim(-150, 150);

