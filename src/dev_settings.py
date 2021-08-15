#pip install beautifulsoup4
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re # regular expression
from datetime import datetime
import pandas as pd 
import time
import os

# Dates to explore
#      Pull existing date map,
str_report_mo_yr = pd.read_csv("date_datamark.csv");
str_report_mo_yr = str_report_mo_yr.iloc[:,0].tolist();

# Date to pull - new months
#str_report_mo_yr_new = ["2021-07"];
# Combine, and root out redundant dates, just in case
str_report_mo_yr = sorted(list(set(str_report_mo_yr + str_report_mo_yr_new)))
#Print back to csv file
pd.DataFrame(str_report_mo_yr, columns =['str_report_mo_yr']).to_csv("date_datamark.csv", index = False)

# Rest of data needed.
str_region = {"mark": ["-su", "-at", "-bo", "-ch", "-cl", "-da", "-kc",
            "-mi", "-ny", "-ph", "-ri", "-sf", "-sl"], 
            "names": ["national", "atlanta", "boston", "chicago", 
                    "cleveland", "dallas", "kansas city", "minneapolis",
                    "new york", "philadelphia", "richmond", "san francisco",
                    "st louis"]
        };
str_region = pd.DataFrame(str_region);
# String directory
str_directory = 'https://www.minneapolisfed.org/beige-book-reports/';