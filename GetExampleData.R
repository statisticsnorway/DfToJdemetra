# ---
# jupyter:
#   jupytext:
#     formats: ipynb,R:percent
#     text_representation:
#       extension: .R
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.13.7
#   kernelspec:
#     display_name: SparkR (local)
#     language: R
#     name: ir
# ---

# %%
library(PxWebApiData)
library(tidyr)

# %%
# Get data from Statistics Norways API about the number of jobs per month. Preliminary figures. 
Jobs <- ApiData2("http://data.ssb.no/api/v0/en/table/13126",
                 Tid = TRUE,
                 ForelopigEndelig = '01',
                 ContentsCode = 'AntArbForhold',
                 NACE2007 = TRUE)

# %%
# Filter out totals and remove unnecessary columns 
JobsPrelim <- Jobs[Jobs$NACE2007 != "00-99",
                  -which(names(Jobs) %in% c("ForelopigEndelig", "ContentsCode"))]

# %%
# Get the data on wide form
JobsPreliminary <- pivot_wider(data = JobsPrelim,
                                      names_from = NACE2007,
                                      values_from = value,
                                      names_prefix = "NA")

# %%
# Write a csv
write.csv(JobsPreliminary,
          "~/JobsPreliminary.csv",
          row.names = FALSE)
