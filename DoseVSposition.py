# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 15:20:11 2022

@author: josste
"""

import PySimpleGUI as sg
import numpy as np
import pydicom
import matplotlib.pyplot as plt
import os
import matplotlib as mpl
import glob

# Layout and window
working_directory = os.getcwd()

layout = [# Importing image series
          [sg.Text('Choose image series')], 
          [sg.InputText('F:/Røntgen/Arbeidsmappe/2022/2022-11 effekt av armposisjon på CT/221109-armposisjon-lab9/DICOM/00003583_sorted by_Series Description/1. Armer langs siden', 
                        key='FOLDER_PATH', enable_events=True), sg.FolderBrowse(initial_folder=working_directory)],
          # Importing topogram
          [sg.Text('Choose topogram')],
          [sg.InputText('F:/Røntgen/Arbeidsmappe/2022/2022-11 effekt av armposisjon på CT/221109-armposisjon-lab9/DICOM/00003583_sorted by_Series Description/Topogram  0.6  T20f/TOPO1-armene ned langs siden', 
                        key='FILE_PATH', enable_events=True), sg.FileBrowse(initial_folder=working_directory, file_types=[('DICOM files', '*.*')])],
          # Importing all topograms
          #[sg.Text('Choose all topograms:')],
          #[sg.InputText(key='TOPOS_PATH', enable_events=True), sg.FilesBrowse(initial_folder=working_directory, file_types=['Folder','*'])],
          # Doseplot
          [sg.Button('Dose(z)', key = 'PLOT', enable_events=True)], # Temporary test button
          # Displaying topogram with doseplot
          [sg.Button('Topogram + Dose(z)', key = 'TOPO', enable_events=True)],
          # All doseplots
          [sg.Button('All dose plots', key='ALL_PLOTS', enable_events=True)]
          ]

window = sg.Window('Dose vs position', layout, size = (500, 300))

# Functions 
def sortImages(pathname):
    '''Function from Vilde
    Sort images in same directory'''
    sortDict = {}
    for path in glob.glob(pathname):
        # Linux use /, while Windows use \. Changee from \ to /
        path = path.replace("\\","/")                                   
        # ds is the dicom file
        ds = pydicom.dcmread(path, stop_before_pixels=True)             
        # Slice location is the key to its dose
        sortDict[ds.SliceLocation] = ds[0x18, 0x1152].value
        mpl.rc('figure', max_open_warning = 0)
        sortedKeys = sorted(sortDict.keys())
    return sortDict, sortedKeys

# GUI action
while True:
    event, values = window.read()  
    
    if event == 'PLOT':
        folder_path = values['FOLDER_PATH']+'/*'
        # Getting position and dose at that position. The position is key to the dict. 
        sort_dose, sortedKeys = sortImages(folder_path)
        
        # Plotting
        plt.figure()
        lists = sorted(sort_dose.items())
        pos, dose = zip(*lists)
        plt.plot(pos, dose)
        plt.xlabel('Position (mm)')
        plt.ylabel('Dose (mAs)')
        plt.show()
    
    if event == 'TOPO':
        topo_path = values['FILE_PATH']
        topo = pydicom.dcmread(topo_path)
        topo_img = pydicom.dcmread(topo_path).pixel_array
        # Croping according to zeros
        x, y = np.nonzero(topo_img)
        xl, xr = x.min(), x.max()
        yl, yr = y.min(), y.max()
        topo_img = topo_img[xl:xr+1, yl:yr+1]
        # rotation
        topo_img = np.rot90(topo_img, 1)
        # Topo start position
        topo_start_position = topo.SliceLocation
        print(f"Topogram start position: {topo_start_position} mm")
        # pixel size
        px_sz = topo[0x28, 0x30]
        px_sz_row = px_sz[0] # pixel row spacing in mm
        px_sz_col = px_sz[1] # pixel column spacing in mm 
        print(f'Size of pixel in x-direction: {px_sz_col} mm')
        print(f'Size of pixel in y-direction: {px_sz_row} mm')
        # Topo pixel 
        # Topo plot
        fig, ax = plt.subplots()
        # image scaling
        x_start = topo_start_position
        x_end = topo_start_position + px_sz_row*topo_img.shape[1]
        y_start = 0
        y_end = px_sz_col*topo_img.shape[0]
        
        print('---------------------------------------')
        print(f'Start position x-axis: {x_start}')
        print(f'End position x-axis: {x_end}')
        print(f'Start position y-axis: {y_start}')
        print(f'End position y-axis: {y_end}')
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        
        im = ax.imshow(topo_img, cmap='Greys_r', extent=[x_start, x_end, y_start, y_end])
        
        folder_path = values['FOLDER_PATH']+'/*'
        # Getting position and dose at that position. The position is key to the dict. 
        sort_dose, sortedKeys = sortImages(folder_path)
        
        # Plotting
        lists = sorted(sort_dose.items())
        pos, dose = zip(*lists)
        plt.plot(pos, dose, 'r-')
        plt.xlabel('Position (mm)')
        plt.ylabel('Dose (mAs)')
        plt.show()
        
    if event == 'ALL_PLOTS':
        '''
        topos_path_list = values['TOPOS_PATH'].split(';')
        print(topos_path_list[0])
        print('-----')
        print(topos_path_list[1])
        print('-----')
        print(topos_path_list[2])
        print('-----')
        print(topos_path_list[3])
        print('-----')'''
        topos_path_list=[]
        topos_path_list.append('F:/Røntgen/Arbeidsmappe/2022/2022-11 effekt av armposisjon på CT/221109-armposisjon-lab9/DICOM/00003583_sorted by_Series Description/1. Armer langs siden/*')
        topos_path_list.append('F:/Røntgen/Arbeidsmappe/2022/2022-11 effekt av armposisjon på CT/221109-armposisjon-lab9/DICOM/00003583_sorted by_Series Description/2. Armer over pute på magen/*')
        topos_path_list.append('F:/Røntgen/Arbeidsmappe/2022/2022-11 effekt av armposisjon på CT/221109-armposisjon-lab9/DICOM/00003583_sorted by_Series Description/3. Armer i kryss over pute på brystkasse/*')
        topos_path_list.append('F:/Røntgen/Arbeidsmappe/2022/2022-11 effekt av armposisjon på CT/221109-armposisjon-lab9/DICOM/00003583_sorted by_Series Description/4. Armer liggende oppå/*')
        
        label_list = ['1. Langs siden', '2. Over pute på mage', '3. I kryss over pute på bryst', '4. Liggende oppå']
        plt.figure()
        # Plotting data from each selected scan
        for i in range(len(topos_path_list)):    
            sort_dose, sortedKeys = sortImages(topos_path_list[i])
            lists = sorted(sort_dose.items())
            pos, dose = zip(*lists)
            plt.plot(pos, dose, label=label_list[i])        
        
        plt.xlabel('Position (mm)')
        plt.ylabel('Dose (mAs)')
        plt.grid()
        plt.legend()
        plt.show()
        
    if event == sg.WIN_CLOSED:
        break
    
window.close()

# Kodeplan
# 1. Ta inn mappe-path for bilder
# 2. Ta inn path til topogram
# 3. Sorter og finn alle bildenavn i mappe-path. I samme funksjon burde det også lages to lister med posisjon og dose.
# 4. Hva er forholdet mellom koordinater i topogram og posisjon i bildeserie?
# 5. Plot Dose vs posisjon
 