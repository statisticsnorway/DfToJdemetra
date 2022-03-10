# Python utilites for working with Jdemetra+

This repo holds some utility-functions written in Python for seasonal adjustment with [Jdemetra+](https://jdemetradocumentation.github.io/JDemetra-documentation/) and [JWSACruncher](https://github.com/jdemetra/jwsacruncher/wiki). 

## From Pandas DataFrame to Jdemetra+ with XML

The function in [./DfToJdemetra.py](https://github.com/statisticsnorway/DfToJdemetra/blob/main/DfToJdemetra.py) is an attempt to make it easier to transform a Pandas DataFrame to an XML-file that can be used as input data for seasonal adjustment with [Jdemetra+](https://jdemetradocumentation.github.io/JDemetra-documentation/) and [JWSACruncher](https://github.com/jdemetra/jwsacruncher/wiki). The XML is then compliant with the specification laid out on [p.15 of this document](https://ec.europa.eu/eurostat/cros/system/files/jdemetra_user_guide.pdf). 

**Step-by-step guide**

1. Import the [jobs.csv](https://github.com/statisticsnorway/DfToJdemetra/blob/main/data/JobsPreliminary.csv) into your python environment. These are monthly figures on the number of jobs in Norway [published by Statistics Norway (SSB)](https://www.ssb.no/en/statbank/table/13126/). The dataset is accessible for everyone via [the SSB API](https://www.ssb.no/en/api). If you wanna collect the data yourself, just run R-script [GetExampleData.R](https://github.com/statisticsnorway/DfToJdemetra/blob/main/GetExampleData.R). 

2. Use Pandas to import the CSV to dataframe:
```python
import pandas as pd
RawSeries = pd.read_csv("./data/JobsPreliminary.csv")
```

