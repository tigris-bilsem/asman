import h5py 
import numpy as np 

# Open the HDF5 file in read-only mode 
with h5py.File('x.hdf', 'r') as f: 
 # List all groups 
 print("Keys: %s" % f.keys()) 
 # Get the object name for the first group 
 a_group_key = list(f.keys())[0] 

 # Get the data 
 data = list(f[a_group_key])
