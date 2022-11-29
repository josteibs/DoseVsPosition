# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 15:20:11 2022

@author: josste
"""

import PySimpleGUI as sg
import pydicom
import matplotlib.pyplot as plt
import os
import matplotlib as mpl
import glob

# Layout and window
working_directory = os.getcwd()

layout = [[sg.Text('Choose image series')], 
          # Button for importing image series
          [sg.InputText('F:/Røntgen/Arbeidsmappe/2022/2022-11 effekt av armposisjon på CT/221109-armposisjon-lab9/DICOM/00003583_sorted by_Series Description/1. Armer langs siden', 
                        key = 'FOLDER_PATH', enable_events=True), sg.FolderBrowse(initial_folder = working_directory)],
          [sg.Text('Choose topogram')],
          # Button for importing topogram
          [sg.InputText('F:/Røntgen/Arbeidsmappe/2022/2022-11 effekt av armposisjon på CT/221109-armposisjon-lab9/DICOM/00003583_sorted by_Series Description/Topogram  0.6  T20f/TOPO1-armene ned langs siden', 
                        key = 'FILE_PATH', enable_events=True), sg.FileBrowse(initial_folder = working_directory, file_types=[('DICOM files', '*.*')])],
          # Testing image plot
          [sg.Button('Dose(z)', key = 'PLOT', enable_events=True)], # Temporary test button
          # Displaying topogram
          [sg.Button('Topogram', key = 'TOPO', enable_events=True)]
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
        print(ds[0x300A, 0x192].value)          
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
        topo_top_position = topo.SliceLocation
        print("Topogram start position: ")
        print(topo_top_position)
        # Topo plot
        fig, ax = plt.subplots()
        plt.gcf().set_facecolor("black")
        ax.imshow(topo_img, cmap='Greys_r')
        
        
    if event == sg.WIN_CLOSED:
        break
    
window.close()

# Kodeplan
# 1. Ta inn mappe-path for bilder
# 2. Ta inn path til topogram
# 3. Sorter og finn alle bildenavn i mappe-path. I samme funksjon burde det også lages to lister med posisjon og dose.
# 4. Hva er forholdet mellom koordinater i topogram og posisjon i bildeserie?
# 5. Plot Dose vs posisjon
 