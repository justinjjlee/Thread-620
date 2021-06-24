#pip install beautifulsoup4
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re # regular expression
from datetime import datetime
import pandas as pd 
import time
import os

from dev_settings import *

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
    "1980-12",
    "1981-01",
    "1981-03",
    "1981-05",
    "1981-06",
    "1981-08",
    "1981-09",
    "1981-11",
    "1981-12",
    "1982-01",
    "1982-03",
    "1982-05",
    "1982-06",
    "1982-08",
    "1982-09",
    "1982-11",
    "1982-12",
    "1983-02",
    "1983-03",
    "1983-05",
    "1983-07",
    "1983-08",
    "1983-09",
    "1983-11",
    "1983-12",
    "1984-01",
    "1984-03",
    "1984-05",
    "1984-06",
    "1984-08",
    "1984-09",
    "1984-10",
    "1984-12",
    "1985-01",
    "1985-03",
    "1985-05",
    "1985-06",
    "1985-08",
    "1985-09",
    "1985-10",
    "1985-12",
    "1986-01",
    "1986-03",
    "1986-05",
    "1986-06",
    "1986-08",
    "1986-09",
    "1986-10",
    "1986-12",
    "1987-01",
    "1987-03",
    "1987-05",
    "1987-06",
    "1987-08",
    "1987-09",
    "1987-10",
    "1987-12",
    "1988-01",
    "1988-03",
    "1988-05",
    "1988-06",
    "1988-08",
    "1988-09",
    "1988-10",
    "1988-11",
    "1989-01",
    "1989-03",
    "1989-05",
    "1989-06",
    "1989-08",
    "1989-09",
    "1989-11",
    "1989-12",
    "1990-01",
    "1990-03",
    "1990-05",
    "1990-06",
    "1990-08",
    "1990-09",
    "1990-10",
    "1990-12",
    "1991-01",
    "1991-03",
    "1991-05",
    "1991-06",
    "1991-08",
    "1991-09",
    "1991-10",
    "1991-12",
    "1992-01",
    "1992-03",
    "1992-05",
    "1992-06",
    "1992-08",
    "1992-09",
    "1992-11",
    "1992-12",
    "1993-01",
    "1993-03",
    "1993-05",
    "1993-06",
    "1993-08",
    "1993-09",
    "1993-11",
    "1993-12",
    "1994-01",
    "1994-03",
    "1994-05",
    "1994-06",
    "1994-08",
    "1994-09",
    "1994-11",
    "1994-12",
    "1995-01",
    "1995-03",
    "1995-05",
    "1995-06",
    "1995-08",
    "1995-09",
    "1995-11",
    "1995-12",
    "1996-01",
    "1996-03",
    "1996-05",
    "1996-06",
    "1996-08",
    "1996-09",
    "1996-10",
    "1996-12",
    "1997-01",
    "1997-03",
    "1997-05",
    "1997-06",
    "1997-08",
    "1997-09",
    "1997-10",
    "1997-12",
    "1998-01",
    "1998-03",
    "1998-05",
    "1998-06",
    "1998-08",
    "1998-09",
    "1998-11",
    "1998-12",
    "1999-01",
    "1999-03",
    "1999-05",
    "1999-06",
    "1999-08",
    "1999-09",
    "1999-11",
    "1999-12",
    "2000-01",
    "2000-03",
    "2000-05",
    "2000-06",
    "2000-08",
    "2000-09",
    "2000-11",
    "2000-12",
    "2001-01",
    "2001-03",
    "2001-05",
    "2001-06",
    "2001-08",
    "2001-09",
    "2001-10",
    "2001-11",
    "2002-01",
    "2002-03",
    "2002-04",
    "2002-06",
    "2002-07",
    "2002-09",
    "2002-10",
    "2002-11",
    "2003-01",
    "2003-03",
    "2003-04",
    "2003-06",
    "2003-07",
    "2003-09",
    "2003-10",
    "2003-11",
    "2004-01",
    "2004-03",
    "2004-04",
    "2004-06",
    "2004-07",
    "2004-09",
    "2004-10",
    "2004-12",
    "2005-01",
    "2005-03",
    "2005-04",
    "2005-06",
    "2005-07",
    "2005-09",
    "2005-10",
    "2005-11",
    "2006-01",
    "2006-03",
    "2006-04",
    "2006-06",
    "2006-07",
    "2006-09",
    "2006-10",
    "2006-11",
    "2007-01",
    "2007-03",
    "2007-04",
    "2007-06",
    "2007-07",
    "2007-09",
    "2007-10",
    "2007-11",
    "2008-01",
    "2008-03",
    "2008-04",
    "2008-06",
    "2008-07",
    "2008-09",
    "2008-10",
    "2008-12",
    "2009-01",
    "2009-03",
    "2009-04",
    "2009-06",
    "2009-07",
    "2009-09",
    "2009-10",
    "2009-12",
    "2010-01",
    "2010-03",
    "2010-04",
    "2010-06",
    "2010-07",
    "2010-09",
    "2010-10",
    "2010-12",
    "2011-01",
    "2011-03",
    "2011-04",
    "2011-06",
    "2011-07",
    "2011-09",
    "2011-10",
    "2011-11",
    "2012-01",
    "2012-02",
    "2012-04",
    "2012-06",
    "2012-07",
    "2012-08",
    "2012-10",
    "2012-11",
    "2013-01",
    "2013-03",
    "2013-04",
    "2013-06",
    "2013-07",
    "2013-09",
    "2013-10",
    "2013-12",
    "2014-01",
    "2014-03",
    "2014-04",
    "2014-06",
    "2014-07",
    "2014-09",
    "2014-10",
    "2014-12",
    "2015-01",
    "2015-03",
    "2015-04",
    "2015-06",
    "2015-07",
    "2015-09",
    "2015-10",
    "2015-12",
    "2016-01",
    "2016-03"
];
# Pull historical file
# 1970-05
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

        # Exception for minneapolis  - 1995
        if timeiter == 'ovember1,1995':
            timeiter = 'November1,1995'
        #timeiter = datetime.date(datetime.strptime(timeiter, '%B %d, %Y'));
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
# Go through and pull data
for idx_region, iter_region in enumerate(str_region.values):

    # Define the complete url
    str_report = [str_directory + iter[0:4] + '/' + iter + iter_region[0] for iter in str_report_mo_yr];
    for idx, iter_url in enumerate(str_report):
        time.sleep(2.5) 

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