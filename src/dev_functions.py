#pip install beautifulsoup4
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re # regular expression
from datetime import datetime
import pandas as pd 
import time
import os

# Pull historical file
# 1970-05
def text_scrap(soupified, str_region):
    txt = soupified.find("div", {"class": "col-sm-12 col-lg-8 offset-lg-1"});
    #blab
    # Pull date
    timeiter = txt.find("strong").get_text().strip();
    timeiter = datetime.date(datetime.strptime(timeiter, '%B %d, %Y'));
    print(timeiter, str_region);

    # Proposed string
    txt_body = txt.find_next("strong").find_next("strong");

    # ROUTE 1: IF THERE IS NO SECTION DEFINED:
    if ((txt_body != None) & (len(txt.findAll("strong")) >= 2)):
        # Need to go through each loop 
        iter_temp = 1;
        #txt.find_next("strong").find_next("p")

        # Point to date record + proposed step
        #txt_body = txt.find_next("strong").find_next("strong");
        txt_body = (txt.find_next("strong").find_next("p"))
        while (txt_body != None):
            # They are divided in section, put up separate df
            # print(txt_body)
            # Bodty of text - including the title
            idx_category = txt_body.find("strong").get_text();

            # If error, it means there is an overall summary
            try:
                idx_category = txt_body.find("strong").get_text();
            except:
                idx_category = "overall";
            # From the block, remove the title spec
            ini_txt = txt_body.get_text().replace(idx_category,'');
            # If there are multiple paragraph
            try: 
                while txt_body.find_next("p").find_all("strong") == []:
                    txt_body = txt_body.find_next("p");
                    ini_txt = ini_txt + " " + txt_body.get_text();
            except:
                end = 1
                # Do nothing

            ini_txt = ini_txt.replace("\r\n",""); # clean up

            # Create data frame
            data = {"time": [timeiter], "region": [str_region], 
                        "category": [idx_category], "text": [ini_txt]};
            # append dataframe
            if iter_temp == 1:
                df = pd.DataFrame(data);
            else:
                df_temp = pd.DataFrame(data);
                df = df.append(df_temp, ignore_index = True);
            
            # Update the next block
            iter_temp = iter_temp + 1;
            txt_body = txt_body.find_next("p")
    else: #if (txt_body == None): 
        # If there is no section defined - put all in one text
        idx_category = "overall"

        # initial text - proposed location
        txt_body = txt.find_next("p").find_next("p").find_next("p"); # where the text starts
        # Start with proposed next text
        ini_txt = txt_body.get_text();
        while txt_body.attrs == {}: # Until reaching the end of the paragraph details
            ini_txt = ini_txt + " " + txt_body.get_text();
            txt_body = txt_body.find_next("p");
        ini_txt = ini_txt.replace("\r\n",""); # Replace
        ini_txt = ini_txt.replace("\n",""); # Replace
        data = {"time": [timeiter], "region": [str_region], 
                "category": [idx_category], "text": [ini_txt]};
        
        # Create DataFrame  
        df = pd.DataFrame(data);
    return df;

# Dates to explore
str_report_mo_yr = [
    "1970-05",
    "1970-06",
    "1970-07",
    "1970-08",
    "1970-09",
    "1970-10",
    "1970-11",
    "1970-12",
    "1971-01",
    "1971-02",
    "1971-03",
    "1971-04",
    "1971-05",
    "1971-06",
    "1971-07",
    "1971-08",
    "1971-09",
    "1971-10",
    "1971-11",
    "1971-12",
    "1972-02",
    "1972-03",
    "1972-04",
    "1972-05",
    "1972-06",
    "1972-07",
    "1972-08",
    "1972-09",
    "1972-10",
    "1972-11",
    "1972-12",
    "1973-01",
    "1973-02",
    "1973-03",
    "1973-04",
    "1973-05",
    "1973-06",
    "1973-07",
    "1973-08",
    "1973-09",
    "1973-10",
    "1973-11",
    "1973-12",
    "1974-01",
    "1974-02",
    "1974-03",
    "1974-04",
    "1974-05",
    "1974-06",
    "1974-07",
    "1974-08",
    "1974-09",
    "1974-10",
    "1974-11",
    "1974-12",
    "1975-01",
    "1975-02",
    "1975-03",
    "1975-04",
    "1975-05",
    "1975-06",
    "1975-07",
    "1975-08",
    "1975-09",
    "1975-10",
    "1975-11",
    "1975-12",
    "1976-01",
    "1976-02",
    "1976-03",
    "1976-04",
    "1976-05",
    "1976-06",
    "1976-07",
    "1976-08",
    "1976-09",
    "1976-10",
    "1976-11",
    "1976-12",
    "1977-01",
    "1977-02",
    "1977-03",
    "1977-04",
    "1977-05",
    "1977-06",
    "1977-07",
    "1977-08",
    "1977-09",
    "1977-10",
    "1977-11",
    "1977-12",
    "1978-01",
    "1978-02",
    "1978-03",
    "1978-04",
    "1978-05",
    "1978-06",
    "1978-07",
    "1978-08",
    "1978-09",
    "1978-10",
    "1978-11",
    "1978-12",
    "1979-01",
    "1979-03",
    "1979-04",
    "1979-05",
    "1979-07",
    "1979-08",
    "1979-09",
    "1979-10",
    "1979-11",
    "1980-01",
    "1980-03",
    "1980-04",
    "1980-05",
    "1980-07",
    "1980-08",
    "1980-09",
    "1980-10",
    "1980-11",
    "1980-12"
]

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

# Initialize
df_fin = 0;
# Go through and pull data
for idx_region, iter_region in enumerate(str_region.values):

    # Define the complete url
    str_report = [str_directory + iter[0:4] + '/' + iter + iter_region[0] for iter in str_report_mo_yr];
    for idx, iter_url in enumerate(str_report):
        time.sleep(3.5) 

        html1 = urlopen(iter_url).read()
        soupified = BeautifulSoup(html1, "html.parser")

        #if idx == 0:
        #    df = text_scrap(soupified, str_region)
        #else:
        #    df = pd.concat([df, text_scrap(soupified, iter_region[1])])
        try:
            #df = pd.concat([df, text_scrap(soupified, iter_region[1])])
            df_fin = df_fin.append(text_scrap(soupified, iter_region[1]), ignore_index = True)
        except: # if starting
            df_fin = text_scrap(soupified, iter_region[1])