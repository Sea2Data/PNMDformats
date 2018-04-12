
from xml.etree import ElementTree as ET
import datetime, time
import numpy as np

    


def indent(elem, level=0):
  '''
  Description: 
       Make the xml file more readable
  '''
  i = "\n" + level*"  "
  if len(elem):
    if not elem.text or not elem.text.strip():
      elem.text = i + "  "
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
    for elem in elem:
      indent(elem, level+1)
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
  else:
    if level and (not elem.tail or not elem.tail.strip()):
      elem.tail = i
      
      


      
      
def addTopLevelInfo(dataset):     
    '''Add top level information '''
    
    
    root = ET.Element("echosounder_dataset")
    ET.SubElement(root,'report_time').text = str(datetime.datetime.fromtimestamp((time.time())).strftime('%Y-%m-%d %H:%M:%S'))
    ET.SubElement(root,'lsss_version').text = "PNMDformats v 0.1"
    ET.SubElement(root,'nation').text = dataset.nation
    ET.SubElement(root,'platform').text = dataset.platform
    ET.SubElement(root,'cruise').text = dataset.cruise 
    return root

    
    
    
    
    
def addLogDistanceInfo(dataset,distance_list,i): 
    '''Add information in the log distance level'''
    
    
    #Get the unix time and convert it to time string
    correct_starttime = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(int(dataset['time_start'][i])))
    correct_stoptime = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(int(dataset['time_end'][i])))
    
    
    
    #Write new log distance with its attributes
    distance = ET.SubElement(distance_list,'distance')
    distance.set('log_start',str(dataset['log_start'][i]))
    distance.set('start_time',correct_starttime)

    
    
    #Add variables to the log distance
    ET.SubElement(distance,'integrator_dist').text = str(dataset['integrator_dist'][i])
    ET.SubElement(distance,'pel_ch_thickness').text = str(dataset['pel_ch_thick'][i])
    try:
        ET.SubElement(distance,'bot_ch_thickness').text = str(dataset['bot_ch_thick'][i])
    except IndexError: 
        print('')
    ET.SubElement(distance,'include_estimate').text = str(dataset['inc_est'][i])
    ET.SubElement(distance,'lat_start').text = str(dataset['lat_start'][i])
    ET.SubElement(distance,'lon_start').text = str(dataset['lon_start'][i])
    ET.SubElement(distance,'lat_stop').text = str(dataset['lat_end'][i])
    ET.SubElement(distance,'lon_stop').text = str(dataset['lon_end'][i])
    ET.SubElement(distance,'stop_time').text = correct_stoptime 
        
        
    return distance
    
    
    
    
    
    
def addFrequencyLevelInfo(distance,freq,tran,dataset,i): 
    '''Add information in the frequency level'''
    
    
    #Make new frequency with attributes
    frequency = ET.SubElement(distance,'frequency')
    frequency.set('freq',str(int(freq))  )
    frequency.set('transceiver',str(int(tran)))
    
    
    #Include all parameters in frequency,ignore those not existing
    ET.SubElement(frequency,'num_pel_ch').text = str(dataset['num_pel_ch'][i])  
    try: 
        ET.SubElement(frequency,'num_bot_ch').text = str(dataset['num_bot_ch'][i])  
        ET.SubElement(frequency,'min_bot_depth').text = str(dataset['min_bot_depth'][i])  
        ET.SubElement(frequency,'max_bot_depth').text = str(dataset['max_bot_depth'][i])  
    except IndexError: 
        print('',end='\r')
    try: 
        ET.SubElement(frequency,'upper_interpret_depth').text = str(dataset['upper_interpret_depth'][i])  
    except IndexError: 
        print('',end='\r')
    try: 
        ET.SubElement(frequency,'lower_interpret_depth').text = str(dataset['lower_interpret_depth'][i])  
    except IndexError: 
        print('',end='\r')
    try: 
        ET.SubElement(frequency,'upper_integrator_depth').text = str(dataset['upper_integrator_depth'][i])  
    except IndexError: 
        print('',end='\r')
    try: 
        ET.SubElement(frequency,'lower_integrator_depth').text = str(dataset['lower_integrator_depth'][i])  
    except IndexError: 
        print('',end='\r')
    

    
    #include paramteres in frequency
    #THis will change with a new netcdf
    for grp in dataset['Regions'].groups: 
        if int(dataset['Regions'][grp]['frequency'][0]) == freq: 
            ET.SubElement(frequency,'quality').text = str(dataset['Regions'][grp]['quality'][i])  
            ET.SubElement(frequency,'bubble_corr').text = str(dataset['Regions'][grp]['bubble_corr'][i])  
            ET.SubElement(frequency,'threshold').text = str(dataset['Regions'][grp]['threshold'][i])
            break
    
    return frequency
    
    
    
    
    
    
    
def addChannelInfo(frequency,chn,acocat_vec,dataset,freq,i):
    '''Add channel information'''
    
    
    #Make new channel type
    ch_type = ET.SubElement(frequency,'ch_type')
    ch_type.set('type',chn[0])
    
    
    #Loop through each acoustic cathegory
    for aco in set(acocat_vec): 
        
        #Loop through each layer
        for grp in dataset['Regions'].groups: 
            
            #If the layer fits the frequency, channeltype and the acoustic cathegory
            if(int(dataset['Regions'][grp]['frequency'][0])==freq): 
                if(dataset['Regions'][grp]['acocat'][0]==aco): 
                    if(dataset['Regions'][grp]['ch_type'][0]!=chn):                                 
                        
                        
                        #Make new sa_by_acoucat
                        sa_by_acocat = ET.SubElement(ch_type,'sa_by_acocat')
                        sa_by_acocat.set('acocat',str(aco))
                        
                        
                        #Write each depth channel
                        for ii in np.arange(len(dataset['Regions'][grp]['sa_by_acocat'][i,:])): 
                            if dataset['Regions'][grp]['sa_by_acocat'][i,ii]>0: 
                                sa_value = ET.SubElement(sa_by_acocat,'sa')
                                sa_value.set('ch',str(ii+1))
                                sa_value.text = str(dataset['Regions'][grp]['sa_by_acocat'][i,ii])
 
                                
                                
                                
                                
                                
def addBottomLevelInfo(root,dataset): 
    '''Add purpose for each acoustic cathegory'''
    
    
    #get the list of all acoustic cathegories
    acocat_list = ET.SubElement(root,'acocat_list')
    
    #loop through each cathegory
    for grp in dataset['Regions'].groups: 
        
        #Write acoustic cathegory
        acocat = ET.SubElement(acocat_list,'acocat')
        acocat.set('acocat',str(dataset['Regions'][grp]['acocat'][0]))
        
        #Write purpuse as attribute
        purpose = ET.SubElement(acocat,'purpose')
        purpose.text = str(dataset['Regions'][grp]['purpose'][0])


    
    
    
    
                                
def writeLUF20(dataset):
    '''
    Description: 
        Protocol to write to the nmd ListUserFile20 (LUF20) file format
        
        
    '''
    
    
    #Get region specific variables
    #It has only been tested on one region. Should test it on multiple regions 
    #With different variables
    freq_vec = [int(dataset['Regions'][grp]['frequency'][0]) for grp in dataset['Regions'].groups]
    tranceiver_vec = [int(dataset['Regions'][grp]['transceiver'][0]) for grp in dataset['Regions'].groups]
    chn_type_vec = [dataset['Regions'][grp]['ch_type'][0][0].decode('utf-8') for grp in dataset['Regions'].groups]
    acocat_vec = [int(dataset['Regions'][grp]['acocat'][0]) for grp in dataset['Regions'].groups]

                  
                  
    
    #Write the top level information of the XML file
    root = addTopLevelInfo(dataset)
    
    
    
    #Make the distance list hirarchy
    distance_list = ET.SubElement(root,'distance_list')
    
    
    
    #Loop through each log distance
    for i in range(len(dataset['time_start'])): 
        
        
        
        #Add the distance information and variables
        distance = addLogDistanceInfo(dataset,distance_list,i)
        
       
        
        #Loop through each unique frequency
        for freq,tran in zip(set(freq_vec),set(tranceiver_vec)): 
            
            
            #Add information and variables in the frequency level
            frequency = addFrequencyLevelInfo(distance,freq,tran,dataset,i)
           
                
                
            #Loop through each uniqe chanel type
            for chn in set(chn_type_vec): 
                
                
                #Add info and variables in the channel level
                addChannelInfo(frequency,chn,acocat_vec,dataset,freq,i)
                

    #add bottom level information
    addBottomLevelInfo(root,dataset)
    
    
    #structure the file nicely
    indent(root)
 
    
    #write the file to xml format
    tree = ET.ElementTree(root)
    tree.write("ListUserFile20.xml", xml_declaration=True, encoding='utf-8', method="xml")
    
    