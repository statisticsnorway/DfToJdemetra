#!/usr/bin/env python
# coding: utf-8

# In[15]:


# Importing libraries
import pandas as pd
import numpy as np
import xml.etree.cElementTree as ET
import lxml
import os
from bs4 import BeautifulSoup


# In[16]:


# Importing test-data
RawSeries = pd.read_csv("./data/JobsPreliminary.csv")


# In[37]:


def DfToXml(data,
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
        data2.text = verdier.to_string(index=False)

    xml_data = ET.tostring(root)  # binary string
    with open('mainpart.xml', 'w') as f:  # Write in file as utf-8
        f.write(xml_data.decode('utf-8'))

    FirstLine = """<?xml version="1.0" encoding="UTF-8"?>"""
    with open("FirstLine.xml", 'w') as f:
        f.write(FirstLine)

    # Concatinating declaration with the rest. Requires Linux OS
    os.system("cat ~/repositories/DfToJdemetra/FirstLine.xml ~/repositories/DfToJdemetra/mainpart.xml > ./data/jobs.xml")

    # Removes temp-files
    os.system("rm -f ~/repositories/DfToJdemetra/FirstLine.xml ~/repositories/DfToJdemetra/mainpart.xml")
    
    # Pretty-printing for Jupyterlab
    return(print(BeautifulSoup(xml_data, "xml").prettify()))


# In[40]:


DfToXml(data = RawSeries,
        pstart = '1',
        ystart = '2016',
        freq = '12')


# In[24]:





# In[ ]:




