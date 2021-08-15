#pip install beautifulsoup4
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re # regular expression
from datetime import datetime
import pandas as pd 
import time
import os

from dev_settings import *

# Given all the original data is pulled, no need for pulling all again.
#   For those wishes to scrap based on own specification, change it to True.
pull_origin = False;

# Clean the data
def text_scrap(soupified, str_region):
    txt = soupified.find("div", {"class": "col-sm-12 col-lg-8 offset-lg-1"});
    #blab
    # Pull date
    
    try:
        timeiter = txt.find("strong").get_text().strip();
        if timeiter == '':
            # Case of 2015-09, look for the next string
            timeiter = txt.find("strong").find_next("strong").get_text().strip();
            # save the next step
            txt_body = txt.find_next("strong").find_next("strong");
        else :
            # Proposed string
            txt_body = txt.find_next("strong").find_next("strong");

        # Just in case, remove spaces
        timeiter = timeiter.replace(" ", "");

        # Exception for minneapolis - 1995 November
        if timeiter == 'ovember1,1995':
            timeiter = 'November1,1995';
        if timeiter == 'April24,200':
            timeiter = 'April24,2002';
        timeiter = datetime.date(datetime.strptime(timeiter, '%B%d,%Y'));
        
    except:
        timeiter = txt.find(["b", "em"]).get_text().strip();
        txt_body = txt.find_next("strong");

        # Just in case, remove spaces
        timeiter = timeiter.replace(" ", "");
        timeiter = datetime.date(datetime.strptime(timeiter, '%B%d,%Y'));
    # Update the status
    print(timeiter, str_region);

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
    
            # If error, it means there is an overall summary
            try:
                idx_category = txt_body.find("strong").get_text();
            except:
                idx_category = "overview";
                # Another way to approach:
                    # The paragraph does not contain the 'strong' title,
                #if txt_body.find("strong") == None: 
                #    # Then it is an overall summary, save as is
                #    idx_category = "overview";
                #    # Get text
                #    txt_body.get_text();
            # From the block, remove the title spec
            ini_txt = txt_body.get_text().replace(idx_category,'');
            
            try: # If there are multiple paragraph
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
        idx_category = "overview"

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

# Initialize
df_fin = 0;
collect_no_url = [' '];
# Collect url did not work - would need to collect them afterwards.
# Go through and pull data
for idx_region, iter_region in enumerate(str_region.values):
    # Define the complete url

    # Select what date frame to pull.
    vec_date = [];
    if pull_origin == True :
        vec_date = str_report_mo_yr
    else:
        vec_date = str_report_mo_yr_new

    str_report = [str_directory + iter[0:4] + '/' + iter + iter_region[0] for iter in str_report_mo_yr];
    for idx, iter_url in enumerate(str_report):
        time.sleep(0.90) 

        # Try to call site.
        try:
            html1 = urlopen(iter_url).read();
        except: # add to the missig link
            try: # replace -su with -national-summary
                iter_url = iter_url.replace('-su', '-national-summary');
                html1 = urlopen(iter_url).read();
            except:
                collect_no_url.append(iter_url)
                continue
        # text formation using BeautifulSoup
        soupified = BeautifulSoup(html1, "html.parser");
        #if idx == 0:
        #    df = text_scrap(soupified, str_region)
        #else:
        #    df = pd.concat([df, text_scrap(soupified, iter_region[1])])
        try:
            #df = pd.concat([df, text_scrap(soupified, iter_region[1])])
            df_fin = df_fin.append(text_scrap(soupified, iter_region[1]), ignore_index = True)
        except: # if starting
            df_fin = text_scrap(soupified, iter_region[1])

# Save the data
if pull_origin == True:
    df_fin.to_csv("data_beigebook.txt", index = False)
else: # pull the data, append, and save the data.
    df_all = pd.read_csv("data_beigebook.txt");
    df_all.append(df_fin, inplace = True);
    df_all.to_csv("data_beigebook.txt", index = False)