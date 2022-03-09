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


# Importings test-data
RawSeries = pd.read_csv("./data/JobsPreliminary.csv")


# In[17]:


# Dropper datokolonnen siden den ikke trengs mer.
RawSeries2 = RawSeries.drop(RawSeries.columns[0], axis=1)
# Bygger filen herfra
root = ET.Element("tsworkspace", attrib={"xmlns" : "eu/tstoolkit:core",
                                      "xmlns:xsd" : "http://www.w3.org/2001/XMLSchema",
                                      "xmlns:xsi" : "http://www.w3.org/2001/XMLSchema-instance"})
timeseries = ET.SubElement(root, 'timeseries')
tscollection = ET.SubElement(timeseries, "tscollection")
tscollection.set('name', 'jobs')
data = ET.SubElement(tscollection, "data")

# Her legges dataene inn under riktige tags og med riktig navn
for (columnName, columnData) in RawSeries2.iteritems():
    ts = ET.SubElement(data, "ts")
    navn = columnName
    ts.set('name', navn)
    tsdata = ET.SubElement(ts, 'tsdata', attrib={"pstart":"1", "ystart":"2016", "freq":"12"})
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


# In[18]:


# Pretty-printing for Jupyterlab
print(BeautifulSoup(xml_data, "xml").prettify())


# In[ ]:




