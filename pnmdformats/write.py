def writeLUF20(dataset):
    '''
    Description: 
        
        
        
    '''
    
    from xml.etree import ElementTree as ET
    import datetime, time
    import numpy as np
    
    
    
    #Function to make the xml file nice
    def indent(elem, level=0):
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
      
      
          
          
    
    #Get attribute of all layers
    freq_vec = [dataset['NMDdata'][grp].frequency for grp in dataset['NMDdata'].groups]
    tranceiver_vec = [dataset['NMDdata'][grp].tranceiver for grp in dataset['NMDdata'].groups]
    chn_type_vec = [dataset['NMDdata'][grp].ch_type for grp in dataset['NMDdata'].groups]
    acocat_vec = [dataset['NMDdata'][grp].acocat for grp in dataset['NMDdata'].groups]



    
    #Initialize file
    root = ET.Element("echosounder_dataset")
    ET.SubElement(root,'report_time').text = str(datetime.datetime.fromtimestamp((time.time())).strftime('%Y-%m-%d %H:%M:%S'))
    ET.SubElement(root,'lsss_version').text = "PNMDformats v 0.1"
    ET.SubElement(root,'nation').text = dataset.nation
    ET.SubElement(root,'platform').text = dataset.platform
    ET.SubElement(root,'cruise').text = dataset.cruise 

    
    
    #Make distance list
    distance_list = ET.SubElement(root,'distance_list')
    
    
    
    #Loop through each log distance
    for i in range(len(dataset['NMDdata']['time_start'])): 
        
        
        #Make new distance with attributes
        distance = ET.SubElement(distance_list,'distance')
        distance.set('log_start',str(dataset['NMDdata']['log_start'][i]))
        distance.set('start_time',str(dataset['NMDdata']['time_start'][i]))

        
        
        #Include parameters in distance
        ET.SubElement(distance,'integrator_dist').text = str(dataset['NMDdata']['int_dist'][i])
        ET.SubElement(distance,'pel_ch_thickness').text = str(dataset['NMDdata']['pel_ch_thick'][i])
        ET.SubElement(distance,'bot_ch_thickness').text = str(dataset['NMDdata']['bot_ch_thick'][i])
        ET.SubElement(distance,'include_estimate').text = str(dataset['NMDdata']['inc_est'][i])
        ET.SubElement(distance,'lat_start').text = str(dataset['NMDdata']['lat_start'][i])
        ET.SubElement(distance,'lon_start').text = str(dataset['NMDdata']['lat_start'][i])
        ET.SubElement(distance,'lat_stop').text = str(dataset['NMDdata']['lat_end'][i])
        ET.SubElement(distance,'lon_stop').text = str(dataset['NMDdata']['lat_end'][i])
        
        
        
        #Loop through each unique frequency
        for freq,tran in zip(set(freq_vec),set(tranceiver_vec)): 
            
            #Make new frequency with attributes
            frequency = ET.SubElement(distance,'frequency')
            frequency.set('freq',freq)  
            frequency.set('transceiver',tran)
            
            
            #Include all parameters in frequency
            ET.SubElement(frequency,'num_pel_ch').text = str(dataset['NMDdata']['num_pel_ch'][i])  
            ET.SubElement(frequency,'num_bot_ch').text = str(dataset['NMDdata']['num_bot_ch'][i])  
            ET.SubElement(frequency,'min_bot_depth').text = str(dataset['NMDdata']['min_bot_depth'][i])  
            ET.SubElement(frequency,'max_bot_depth').text = str(dataset['NMDdata']['max_bot_depth'][i])  
            ET.SubElement(frequency,'upper_interpret_depth').text = str(dataset['NMDdata']['upper_interpret_depth'][i])  
            ET.SubElement(frequency,'lower_interpret_depth').text = str(dataset['NMDdata']['lower_interpret_depth'][i])  
            ET.SubElement(frequency,'upper_integrator_depth').text = str(dataset['NMDdata']['upper_integrator_depth'][i])  
            ET.SubElement(frequency,'lower_integrator_depth').text = str(dataset['NMDdata']['lower_integrator_depth'][i])  
            

            
            #include paramteres in frequency
            #THis will change with a new netcdf
            for grp in dataset['NMDdata'].groups: 
                if dataset['NMDdata'][grp].frequency == freq: 
                    ET.SubElement(frequency,'quality').text = str(dataset['NMDdata'][grp]['quality'][i])  
                    ET.SubElement(frequency,'bubble_corr').text = str(dataset['NMDdata'][grp]['bubble_corr'][i])  
                    ET.SubElement(frequency,'threshold').text = str(dataset['NMDdata'][grp]['threshold'][i])
                    break
                
                
            #Loop through each uniqe chanel type
            for chn in set(chn_type_vec): 
                
                
                #Make new channel type
                ch_type = ET.SubElement(frequency,'ch_type')
                ch_type.set('type',chn[0])
                
                
                #Loop through each acoustic cathegory
                for aco in set(acocat_vec): 
                    
                    #Loop through each layer
                    for grp in dataset['NMDdata'].groups: 
                        
                        #If the layer fits the frequency, channeltype and the acoustic cathegory
                        if(dataset['NMDdata'][grp].frequency==freq): 
                            if(dataset['NMDdata'][grp].acocat==aco): 
                                if(dataset['NMDdata'][grp].ch_type==chn): 
                                
                                    #Make new sa_by_acoucat
                                    sa_by_acocat = ET.SubElement(ch_type,'sa_by_acocat')
                                    sa_by_acocat.set('acocat',aco)   
                                    
                                    
                                    #Write each depth channel
                                    for ii in np.arange(len(dataset['NMDdata'][grp]['sa_by_acocat'][:,i])): 
                                        if dataset['NMDdata'][grp]['sa_by_acocat'][ii,i]>0: 
                                            sa_value = ET.SubElement(sa_by_acocat,'sa')
                                            sa_value.set('ch',str(ii+1))
                                            sa_value.text = str(dataset['NMDdata'][grp]['sa_by_acocat'][ii,i])

                                        
                                        
    #Add purpose for each acoustic cathegory
    acocat_list = ET.SubElement(root,'acocat_list')
    
    for grp in dataset['NMDdata'].groups: 
        acocat = ET.SubElement(acocat_list,'acocat')
        acocat.set('acocat',str(dataset['NMDdata'][grp].acocat))
        
        purpose = ET.SubElement(acocat,'purpose')
        purpose.text = dataset['NMDdata'][grp].purpose

    indent(root)
 
    tree = ET.ElementTree(root)
     
    tree.write("ListUserFile20.xml", xml_declaration=True, encoding='utf-8', method="xml")
