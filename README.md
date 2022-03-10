# Python utilites for working with Jdemetra+

This repo holds some utility-functions written in Python for seasonal adjustment with [Jdemetra+](https://jdemetradocumentation.github.io/JDemetra-documentation/) and [JWSACruncher](https://github.com/jdemetra/jwsacruncher/wiki). 

## From Pandas DataFrame to Jdemetra+ with XML

The function in [./DfToJdemetra.py](https://github.com/statisticsnorway/DfToJdemetra/blob/main/DfToJdemetra.py) is an attempt to make it easier to transform a Pandas DataFrame to an XML-file that can be used as input data for seasonal adjustment with [Jdemetra+](https://jdemetradocumentation.github.io/JDemetra-documentation/) and [JWSACruncher](https://github.com/jdemetra/jwsacruncher/wiki). The XML is then compliant with the specification laid out on [p.15 of this document](https://ec.europa.eu/eurostat/cros/system/files/jdemetra_user_guide.pdf). 

**Step-by-step guide**

1. Import the [jobs.csv](https://github.com/statisticsnorway/DfToJdemetra/blob/main/data/JobsPreliminary.csv) into your python environment. These are monthly figures on the number of jobs in Norway [published by Statistics Norway (SSB)](https://www.ssb.no/en/statbank/table/13126/).[^1]

[^1]: The dataset is accessible for everyone via [the SSB API](https://www.ssb.no/en/api). If you wanna collect the data yourself, just run R-script [GetExampleData.R](https://github.com/statisticsnorway/DfToJdemetra/blob/main/GetExampleData.R). Run this code: 

```python
import pandas as pd
RawSeries = pd.read_csv("./data/JobsPreliminary.csv")
```

2. Load the function: 

```python
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
```

As you can see the file path in the os.system-calls are hard-coded. This will be improved shortly. In the meantime, just the write the correct path that you are using.

Also, we assume that the first column in your data is date/period-column. Thats the reason we drop this in the first line of the function. This will also be improved in the near future. 

3. Pass arguments to the function

Our datasets consists of monthly data starting from january 2016 until january 2022. Hence we pass in these values into the arguments: 

```python
DfToXml(data = RawSeries,
        pstart = '1',
        ystart = '2016',
        freq = '12')
```
