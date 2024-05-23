"""
Inputs: ***.dat files generated by QD-MPMS3. First few points should be measured in high field for diamagnetic background correction.
Parameters: folderpath, subfolder, headers, points
Program output: Field(H) & background corrected Moment(M) data in corresponding *_MH_Corrected.dat files in subfolder.
"""
folderpath = 'C:/Users/mishra/Downloads/MPMS3' #Location of inputs
subfolder = 'MH_Corrected' #Subfolder name for outputs
headers = 45 #Number of headers in MPMS3 data file i.e lines to ignore when importing
points = 5 #Number of initial data points to be used for background slope calculation

import numpy as np #For importing and manipulating data
import os #For changing and creating folders
import shutil #For deleting folders already present
import glob #For batch importing files
from scipy.stats import linregress #For linear slope fit

os.chdir(folderpath)#Changes directory to folderpath
shutil.rmtree(subfolder, ignore_errors=True) #Deletes subfolder if already present
os.mkdir(subfolder) #Creates subfolder
files = glob.glob('*.dat') #Imports filenames with .dat extension
filecount = len(files)  #Counts number of files in folderpath

print(f'The following {filecount} files will be processed:')
print(files) #Prints name of all files to be processed

for i in range(filecount): #Loops through all files
    data_raw = np.loadtxt(files[i], delimiter=',', skiprows=headers, usecols=[3,4]) #Loads column 3 (H) and 4 (M) from MPMS3 .dat files
    #Background correction
    M_bg = data_raw[:points,1] #Selects M values for background correction
    H_bg = data_raw[:points,0] #Selects H values for background correction
    fit = linregress(H_bg, M_bg) #Fits selected M and H values to linear function
    slope = fit.slope #Obtains slope of the linear fit
    M = data_raw[:,1] - slope*data_raw[:,0] #Generates corrected M values by subtracting slope*H
    data = np.column_stack((data_raw[:,0],M)) #Makes array of H and corrected M
    #Saving corrected data
    filename = ''.join(files[i].split())[:-4] #Removes last 4 characters (.dat) from filename.
    filepath = f'{folderpath}/{subfolder}/{filename}_{subfolder}.dat' #Creates name and location of output
    np.savetxt(filepath, data)  #Saves corrected MH data in subfolder

print("All files were processed succesfully. Background corrected MH data files were saved.")