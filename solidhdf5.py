import h5py
import numpy as np

#function for getting dataset names and paths
def show():
    try:
        #sets file
        f = h5py.File('mytestfile.hdf5', 'r')
        groups = f.keys()
        print('Samples:')
        for group in groups:
            print()
            print()
            grpattrs = f[group].attrs
            grpattrsnames = list(grpattrs.keys())
            grpattrsstr = [grpattrname + ': ' + grpattrs[grpattrname] for grpattrname in grpattrsnames]
            print('\t'+'Samplename: '+group)
            print('\t'+', '.join(grpattrsstr))
            print()
            print('\t'+'\t'+'Datasets in sample directory:')
            dsets = list(f[group])
            print()
            for dset in dsets:
                print('\t'+'\t'+'\t'+'/'+dset)
                dsetsattrs = f[group+'/'+dset].attrs
                dsetattrsnames = list(dsetsattrs.keys())
                dsetattrsstr = [dsetattrname + ': ' + dsetsattrs[dsetattrname] for dsetattrname in dsetattrsnames]
                print('\t'+'\t'+'\t'+', '.join(dsetattrsstr))
                print('\t'+'\t'+'\t'+'Load with sah.load('+group+'/'+dset+')')
                print()
    except IOError:
        print("File not accessible.")
    
#function for loading data
def load(pathname):
    try:
        #sets file
        f = h5py.File('mytestfile.hdf5', 'r')
        dset = f.get(pathname)
        npdata = np.array(dset)
        f.close()
        return npdata
    except IOError:
        print("File not accessible.")

#function that writes to file, but doesn't overwrite
def store(npdata,axisnames,project,material,method,date,time,samplename,datasetname):
    
    #path and dataset name---------------------------------------------
    dsetname = datasetname
    pathname = samplename + '/' + dsetname
    
    #creates file
    f = h5py.File('mytestfile.hdf5', 'a')
    f.close()
    
    #Checking file so as to not owerwrite it---------------------------
    #sets file
    f = h5py.File('mytestfile.hdf5', 'r')
    
    groups = f.keys()
    dsets = []
    
    c1 = 0
    c2 = 0
    if samplename in groups:
        c1 = 1
        print('Sample allready has a directory.')
        dsets = f[samplename].keys()
        if dsetname in dsets:
            c2 = 1
            print('Name of dataset is not unique.')
        else:
            print('Name of dataset is unique.')
        
    else:
        print('New sample.')
    
    f.close()
    
    if c2 == 1:
        print('Exiting.')
        return
    
    #Storing data to file---------------------------------------------
    #sets file
    f = h5py.File('mytestfile.hdf5', 'a')
    
    
    #If new group
    if c1 == 0:
        print('Creating new directory and dataset.')
        grp = f.create_group(samplename)
        grp.attrs['Material'] = material
        grp.attrs['Project'] = project
    else:
        print('Adding dataset to sample directory.')
    
    
    dset = f.create_dataset(pathname,data=npdata)
    dset.attrs['Axisnames'] = axisnames
    dset.attrs['Date'] = date
    dset.attrs['Time'] = time
    dset.attrs['Method'] = method
    
    print('Stored as', pathname)
    f.close()
