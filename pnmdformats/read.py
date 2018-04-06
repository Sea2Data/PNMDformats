def readNMD(file_name):

    from  netCDF4 import Dataset
       
    dataset = Dataset(file_name,'r',format = 'NETCDF4')
    
    
    return dataset; 