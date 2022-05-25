'''
The utility module is a module for storing and loading matrix data in the HDF5 format.

The utility module is a collection of functions to store data in backup files, load that data, and show the structure of the storage for the Swedish half of the Solid ALiBI project.
Requires H5py and numpy.
'''

import h5py
import numpy as np

def show(filename):
    '''
    Retrieve and print dataset names and path names.
    
    Parameters
    ----------
    filename : string
        The file in which the data will be stored
    
    Examples
    --------
    >>> solidhdf5.show("existingfile.hdf5")
    Samples:
	Samplename: EA0000
	Material: PTMChmw, Project: testproject
		Datasets in sample directory:
			/PESlt1
			Axisnames: [R,G,B], Date: 20210223, Method: PES, Time: 08:30
			Load with sah.load(EA0000/PESlt1)
			/PESlt_aft_dep1
			Axisnames: [R,G,B], Date: 20210222, Method: PES, Time: 08:31
			Load with sah.load(EA0000/PESlt_aft_dep1)
	Samplename: EA0001
	Material: PTMC, Project: testproject
		Datasets in sample directory:
			/XPShome1
			Axisnames: [R,G,B], Date: 20210222, Method: XPS, Time: 08:32
			Load with sah.load(EA0001/XPShome1)
    
    >>> solidhdf5.show("nonexistingfile.hdf5")
    File not accessible.
    '''
    try:
        #sets file
        f = h5py.File(filename, 'r')
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
    

def load(filename,pathname):
    '''
    Loads data from the specified path.
    
    Parameters
    ----------
    
    filename : string
        The file in which the data will be stored.
    pathname : string
        The name of the path that is to be loaded.
            
    Returns
    -------
        out : ndarray
            A numpy array with the data of the specified dataset at the specified path.
    
    Examples
    --------
    >>> data1 = solidhdf5.load(filename,'examplesamplename/exampledatasetname')
    >>> print(data1)
    [[0.21564463 0.75646396 0.12075528]
     [0.12366514 0.30159192 0.5984904 ]
     [0.36632133 0.70121912 0.72520193]
     [0.60009395 0.95945118 0.4504172 ]
     [0.09609428 0.93104292 0.58154557]
     [0.70153355 0.26866447 0.94339851]
     [0.30996851 0.815849   0.6650549 ]
     [0.77609404 0.03327819 0.27019772]
     [0.88414155 0.17683762 0.21253595]
     [0.34329545 0.03850023 0.40853051]]
     
    >>> data2 = solidhdf5.load(filename,'nonexistingfilename')
    No data in the specified path
    '''
    try:
        #sets file
        f = h5py.File(filename, 'r')
        dset = f.get(pathname)
        if dset == None:
            print('No data in the specified path')
        else:
            npdata = np.array(dset)
            f.close()
            return npdata
    except IOError:
        print("File not accessible.")

def store(filename,npdata,axisnames,project,material,method,date,time,samplename,datasetname):
    '''
    Store data in the hdf5 file, without overwriting previous data.
    Pathname is generated as the samplename plus the name of the dataset.
    
    Parameters
    ----------
    
    filename : string
        The file in which the data will be stored
                    
    npdata : array_like
        The data which is to be stored
                    
    axisnames : string array
        The names of the axises of the data
                    
    project : string
        Name of the project
                    
    material : string
        Name of the material that is studied
                    
    method : string
        Name of the method used to obtain the data
                    
    date : string
        Date of data aquisition
                    
    time : string
        Experiment start time
                    
    samplename : string
        Name of the sample
                    
    datasetname : string
        Name of the dataset
                    
    Examples
    --------
    >>> solidhdf5.store(filename,a1,'[R,G,B]','testproject','PTMChmw','PES','20210223','08:30','EA0000','PESlt1')
    New sample.
    Creating new directory and dataset.
    Stored as EA0000/PESlt1
    
    >>> sah.store(filename,a2,'[R,G,B]','testproject','PTMChmw','PES','20210222','08:31','EA0000','PESlt_aft_dep1')
    Sample already has a directory.
    Name of dataset is unique.
    Adding dataset to sample directory.
    Stored as EA0000/PESlt_aft_dep1
    
    >>> sah.store(filename,a2,'[R,G,B]','testproject','PTMChmw','PES','20210222','08:31','EA0000','PESlt_aft_dep1')
    Sample already has a directory.
    Name of dataset is not unique.
    Did not store data.
    '''
    #path and dataset name---------------------------------------------
    dsetname = datasetname
    pathname = samplename + '/' + dsetname
    
    #creates file
    f = h5py.File(filename, 'a')
    f.close()
    
    #Checking file so as to not owerwrite it---------------------------
    #sets file
    f = h5py.File(filename, 'r')
    
    groups = f.keys()
    dsets = []
    
    c1 = 0
    c2 = 0
    if samplename in groups:
        c1 = 1
        print('Sample already has a directory.')
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
        print('Did not store data.')
        return
    
    #Storing data to file---------------------------------------------
    #sets file
    f = h5py.File(filename, 'a')
    
    
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
