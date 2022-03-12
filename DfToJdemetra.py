# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.7
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

import pandas as pd
import xml.etree.cElementTree as ET
import os
from bs4 import BeautifulSoup


def DfToXml(data,
            out : str,
            outpath : str,
            pstart : str,
            ystart : str,
            freq : str):
    """
    Parameters:
        data : A Pandas DataFrame you want to convert.
        out : The name of the outputfile and attribute name in tscollection.
        outpath : Directory you want to save the output-file.
        pstart : The period (month, quarter) you want the sa to start in the first year.
        ystart : Startyear of the series.
        freq : Yearly frequency of the series. Quarterly is 4, monthly is 12, etc..

    Returns:
        An XML-file in your specified directory.
    """
    # Deletes the first column since its because in our data thats a period-column
    RawSeries2 = data.drop(data.columns[0], axis=1)
    # Start building xml
    root = ET.Element("tsworkspace", attrib={"xmlns": "eu/tstoolkit:core",
                                          "xmlns:xsd": "http://www.w3.org/2001/XMLSchema",
                                          "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"})
    timeseries = ET.SubElement(root, 'timeseries')
    tscollection = ET.SubElement(timeseries, "tscollection")
    tscollection.set('name', out)
    data = ET.SubElement(tscollection, "data")

    # Looping through colname and series
    for (columnName, columnData) in RawSeries2.iteritems():
        ts = ET.SubElement(data, "ts")
        navn = columnName
        ts.set('name', navn)
        tsdata = ET.SubElement(ts, 'tsdata', attrib={"pstart": pstart, "ystart": ystart, "freq": freq})
        data2 = ET.SubElement(tsdata, "data")
        verdier = columnData
        verdier2 = verdier.to_string(index=False)
        verdier3 = verdier2.replace("\n", " ")
        data2.text = verdier3

    xml_data = ET.tostring(root)
    xml_data2 = BeautifulSoup(xml_data, "xml").prettify()
    with open(f"{outpath}/{out}.xml", 'w') as f:
        f.write(xml_data2)

    #return print(xml_data2)
    return print(f"""Pandas DataFrame has been converted to an XML and has 
    been saved at {outpath}/{out}.xml""")
