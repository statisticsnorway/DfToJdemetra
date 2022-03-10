#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Importing libraries
import pandas as pd
import xml.etree.cElementTree as ET
import os
from bs4 import BeautifulSoup


# In[ ]:


# Importing test-data
RawSeries = pd.read_csv("./data/JobsPreliminary.csv")


# In[ ]:


def DfToXml(data,
            out : str,
            pstart : str,
            ystart : str,
            freq : str):
    # Deletes the first column since its because in our data thats a period-column
    RawSeries2 = data.drop(data.columns[0], axis=1)
    # Start building xml
    root = ET.Element("tsworkspace", attrib={"xmlns" : "eu/tstoolkit:core",
                                          "xmlns:xsd" : "http://www.w3.org/2001/XMLSchema",
                                          "xmlns:xsi" : "http://www.w3.org/2001/XMLSchema-instance"})
    timeseries = ET.SubElement(root, 'timeseries')
    tscollection = ET.SubElement(timeseries, "tscollection")
    tscollection.set('name', 'jobs')
    data = ET.SubElement(tscollection, "data")

    # Looping through colname and series
    for (columnName, columnData) in RawSeries2.iteritems():
        ts = ET.SubElement(data, "ts")
        navn = columnName
        ts.set('name', navn)
        tsdata = ET.SubElement(ts, 'tsdata', attrib={"pstart":pstart, "ystart":ystart, "freq":freq})
        data2 = ET.SubElement(tsdata, "data")
        verdier = columnData
        verdier2 = verdier.to_string(index=False)
        verdier3 = verdier2.replace("\n", " ")
        data2.text = verdier3

    xml_data = ET.tostring(root)
    xml_data2 = BeautifulSoup(xml_data, "xml").prettify()
    with open('mainpart.xml', 'w') as f:  
        f.write(xml_data2)
        
    FirstLine = """<?xml version="1.0" encoding="UTF-8"?>"""
    with open("FirstLine.xml", 'w') as f:
        f.write(FirstLine)
    
    #command = f"cat ~/repositories/DfToJdemetra/FirstLine.xml ~/repositories/DfToJdemetra/mainpart.xml > ./data/{out}.xml"
    # Concatinating declaration with the rest. Requires Linux OS
    os.system(f"cat ~/repositories/DfToJdemetra/FirstLine.xml ~/repositories/DfToJdemetra/mainpart.xml > ./data/{out}.xml")

    # Removes temp-files
    os.system("rm -f ~/repositories/DfToJdemetra/FirstLine.xml ~/repositories/DfToJdemetra/mainpart.xml")
    
    return print(xml_data2)


# In[ ]:


DfToXml(data = RawSeries,
        out = 'jobs',
        pstart = '1',
        ystart = '2016',
        freq = '12')

