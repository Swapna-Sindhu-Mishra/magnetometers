"""
Inputs: *.dat files generated by QD-MPMS3.
Parameters: folderpath, subfolder, headers
Program output: Field(H) & Moment(M) data in corresponding *_MH.dat files in subfolder.
"""
folderpath = 'C:/Users/mishra/Downloads/MPMS3' #Location of inputs
subfolder = 'MH_Extracted' #Subfolder name for outputs
headers = 28  ##Number of headers in MPMS3 data file i.e lines to ignore when importing

import numpy as np #For importing data
import os #For changing and creating folders
import shutil #For deleting folders already present
import glob #For batch importing files

os.chdir(folderpath) #Changes directory to folderpath
shutil.rmtree(subfolder, ignore_errors=True) #Deletes subfolder if already present
os.mkdir(subfolder) #Creates subfolder
files = glob.glob('*.dat') #Imports filenames with .dat extension
filecount = len(files) #Counts number of files in folderpath

print(f'The following {filecount} files will be extracted:')
print(files) #Prints name of all files to be processed

for i in range(filecount): #Loops through all files.
    #MH data processing
    data_raw = np.loadtxt(files[i], delimiter=',', skiprows=headers, usecols=[3,4]) #Loads column 3 (H) and 4 (M) from MPMS3 .dat files
    data = np.column_stack((data_raw[:,0],data_raw[:,1])) #Creates an array of MH data
    filename = ''.join(files[i].split())[:-4] #Removes last 4 characters (.dat) from filename.
    filepath = f'{folderpath}/{subfolder}/{filename}_{subfolder}_MH.dat' #Creates name and location of output
    np.savetxt(filepath, data, delimiter='\t')  #Saves extracted MH data in subdirectory

print("All files were processed succesfully. MH data files were saved.")