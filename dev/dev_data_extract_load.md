```python
#pip install beautifulsoup4
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re # regular expression
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from string import punctuation
import string
from sklearn.feature_extraction.text import CountVectorizer

from datetime import datetime
import pandas as pd 
import numpy as np
import os
import time
cwd = os.getcwd(); print(cwd)

# Run below to 
#%run dev_functions.py # last error 1980-09
```

### Resources
[Python - BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#getting-help)

## Summary of Commentary on Current Economic Conditions by Federal Reserve District
### Data sources
- [Federal Reserve - Board Archive](https://www.federalreserve.gov/monetarypolicy/beige-book-archive.htm)
- Archive from the [Federal Reserve Bank of Minneapolis](https://www.minneapolisfed.org/region-and-community/regional-economic-indicators/beige-book-archive)  
    - Archive [List - National Summary](https://www.minneapolisfed.org/region-and-community/regional-economic-indicators/beige-book-archive)

### Data pull


```python
# Insert new dates to be collected
str_report_mo_yr_new = ["2021-07"];
```


```python
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


# Given all the original data is pulled, no need for pulling all again.
#   For those wishes to scrap based on own specification, change this to True.
pull_origin = False;

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

    str_report = [str_directory + iter[0:4] + '/' + iter + iter_region[0] for iter in vec_date];
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
    df_all = df_all.append(df_fin);
    df_all.to_csv("data_beigebook.txt", index = False)
```

    2021-07-14 national
    2021-07-14 atlanta
    2021-07-14 boston
    2021-07-14 chicago
    2021-07-14 cleveland
    2021-07-14 dallas
    2021-07-14 kansas city
    2021-07-14 minneapolis
    2021-07-14 new york
    2021-07-14 philadelphia
    2021-07-14 richmond
    2021-07-14 san francisco
    2021-07-14 st louis
    

## Optional: Automation & Deployment
* Google Colab - Cloud Computing and Scheduler
    * Load from Existing data - BigQuery
    * Load from local excel files for data cleaning process
    * Append newer data into BigQuery
* Google BigQuery - Data push automatically and ready available
    * [Python Wrapper](https://cloud.google.com/blog/topics/developers-practitioners/bigquery-explained-data-ingestion)
    * Find an option to append


```python
df_fin = pd.read_csv("data_beigebook.txt")
# Process desk files
df_fin['section'] = [str(each_entry).lower() for each_entry in df_fin['category']];
df_fin['section'] = [str(each_entry).replace("\n", "") for each_entry in df_fin['section']];
df_fin['section'] = [str(each_entry).strip() for each_entry in df_fin['section']];

df_fin[['section']].value_counts()

# Evaluate what goes in 
#df_fin['category'].value_counts().nlargest(20)

# Join with matched for higher level overview
df_fin_match = pd.read_csv("data_beigebook_match.csv", dtype =str)
df_fin = pd.merge(df_fin, df_fin_match, how = 'left', on= 'section')

#df_fin.loc[(df_fin['section'] == '28-Jan-81'), "text"].iloc[0]

list(df_fin.columns)
```




    ['time', 'region', 'category', 'text', 'section', 'count', 'section_overview']




```python
df_fin[['region','section_overview']].value_counts()
```




    region         section_overview                              
    national       overview                                          882
    kansas city    agriculture and natural resource                  534
    minneapolis    agriculture and natural resource                  483
    cleveland      manufacturing and other business activity         467
    richmond       manufacturing and other business activity         429
                                                                    ... 
    san francisco  business activity                                   6
    minneapolis    business activity                                   6
    new york       agriculture and natural resource                    4
    minneapolis    minority- and women-owned business enterprises      3
    atlanta        business sentiment and outlook                      1
    Length: 126, dtype: int64




```python
df_fin.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>time</th>
      <th>region</th>
      <th>category</th>
      <th>text</th>
      <th>section</th>
      <th>count</th>
      <th>section_overview</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1970-05-20</td>
      <td>national</td>
      <td>overview</td>
      <td>This initial report of economic conditions in ...</td>
      <td>overview</td>
      <td>4511</td>
      <td>overview</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1970-06-17</td>
      <td>national</td>
      <td>overview</td>
      <td>Comments on economic conditions in the twelve ...</td>
      <td>overview</td>
      <td>4511</td>
      <td>overview</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1970-07-15</td>
      <td>national</td>
      <td>overview</td>
      <td>Current comment by businessmen and bankers, as...</td>
      <td>overview</td>
      <td>4511</td>
      <td>overview</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1970-08-12</td>
      <td>national</td>
      <td>overview</td>
      <td>The consensus of the reports by the twelve Fed...</td>
      <td>overview</td>
      <td>4511</td>
      <td>overview</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1970-09-09</td>
      <td>national</td>
      <td>overview</td>
      <td>The reports in this Redbook are more optimisti...</td>
      <td>overview</td>
      <td>4511</td>
      <td>overview</td>
    </tr>
  </tbody>
</table>
</div>



## Example of extracting features

1. Vectorizer - use of n-grams
2. Create array of sentences
3. [PoS (Part-of-Speech) tagging](https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html)


```python
tst = ''.join(df_fin.loc[(df_fin.time == '1970-06-17'), 'text_clean'])
str_txt = sent_tokenize(tst)
str_txt[0:5]
```




    ['comments on economic conditions in the twelve federal reserve districts indicate that in most districts bankers and businessmen find economic activity has been weakening, and they generally expected the decline will continue.',
     'in virtually all districts, unemployment is rising, and in many, labor markets are easing noticeably.',
     'retail trade is weaker almost everywhere, and consumers are "downgrading" and bargain-hunting.',
     'a few districts report large cuts in capital spending.',
     'in a number of districts, special note was made of the profit squeeze that is affecting many businesses, and in some, concern was expressed about a decline in corporate liquidity.']




```python
nltk.pos_tag(word_tokenize(str_txt[0]))
```




    [('comments', 'NNS'),
     ('on', 'IN'),
     ('economic', 'JJ'),
     ('conditions', 'NNS'),
     ('in', 'IN'),
     ('the', 'DT'),
     ('twelve', 'JJ'),
     ('federal', 'JJ'),
     ('reserve', 'NN'),
     ('districts', 'NNS'),
     ('indicate', 'VBP'),
     ('that', 'IN'),
     ('in', 'IN'),
     ('most', 'JJS'),
     ('districts', 'NNS'),
     ('bankers', 'NNS'),
     ('and', 'CC'),
     ('businessmen', 'NNS'),
     ('find', 'VBP'),
     ('economic', 'JJ'),
     ('activity', 'NN'),
     ('has', 'VBZ'),
     ('been', 'VBN'),
     ('weakening', 'VBG'),
     (',', ','),
     ('and', 'CC'),
     ('they', 'PRP'),
     ('generally', 'RB'),
     ('expected', 'VBD'),
     ('the', 'DT'),
     ('decline', 'NN'),
     ('will', 'MD'),
     ('continue', 'VB'),
     ('.', '.')]




```python
tst = ''.join(df_fin.loc[(df_fin.time == '1970-06-17'), 'text_clean'])
str_txt = sent_tokenize(tst)

count_vect = CountVectorizer(analyzer='word', ngram_range=(2, 3))
bow_rep = count_vect.fit_transform(str_txt)

bow_rep.toarray()
count_vect.vocabulary_
```




     policy': 8557,
     'in only': 5988,
     'only one': 9035,
     'one federal': 8992,
     'reserve district': 10568,
     'district st': 3784,
     'st louis': 11505,
     'louis was': 7297,
     'was recent': 14152,
     'recent economic': 10181,
     'activity regarded': 221,
     'regarded as': 10336,
     'as good': 1381,
     'good and': 5181,
     'in kansas': 5929,
     'kansas city': 6895,
     'city it': 2624,
     'it was': 6806,
     'was deemed': 14111,
     'deemed fair': 3403,
     'fair to': 4462,
     'to good': 13365,
     'in only one': 5989,
     'only one federal': 9037,
     'one federal reserve': 8993,
     'federal reserve district': 4532,
     'reserve district st': 10571,
     'district st louis': 3785,
     'st louis was': 11507,
     'louis was recent': 7298,
     'was recent economic': 14153,
     'recent economic activity': 10182,
     'economic activity regarded': 3997,
     'activity regarded as': 222,
     'regarded as good': 10338,
     'as good and': 1382,
     'good and in': 5182,
     'and in kansas': 711,
     'in kansas city': 5930,
     'kansas city it': 6898,
     'city it was': 2625,
     'it was deemed': 6808,
     'was deemed fair': 14112,
     'deemed fair to': 3404,
     'fair to good': 4463,
     'districts activity': 3802,
     'has weakened': 5401,
     'weakened significantly': 14191,
     'significantly and': 11182,
     'and decline': 626,
     'in new': 5977,
     'new orders': 8087,
     'orders was': 9160,
     'was noted': 14146,
     'noted in': 8284,
     'in three': 6173,
     'three districts': 13143,
     'most districts activity': 7953,
     'districts activity has': 3803,
     'activity has weakened': 211,
     'has weakened significantly': 5402,
     'weakened significantly and': 14192,
     'significantly and decline': 11183,
     'and decline in': 627,
     'decline in new': 3364,
     'in new orders': 5978,
     'new orders was': 8093,
     'orders was noted': 9161,
     'was noted in': 14147,
     'noted in three': 8287,
     'in three districts': 6175,
     'expectations of': 4332,
     'of further': 8529,
     'further decline': 5035,
     'decline are': 3354,
     'are widespread': 1306,
     'expectations of further': 4333,
     'of further decline': 8530,
     'further decline are': 5036,
     'decline are widespread': 3355,
     'these range': 12980,
     'range however': 10049,
     'however from': 5690,
     'from the': 4980,
     'the belief': 12202,
     'belief that': 2021,
     'that the': 12121,
     'the bottom': 12216,
     'bottom will': 2118,
     'will come': 14447,
     'come in': 2675,
     'the third': 12761,
     'third or': 13043,
     'or fourth': 9099,
     'fourth quarter': 4915,
     'quarter of': 10016,
     'of this': 8800,
     'this year': 13108,
     'year to': 14675,
     'to the': 13517,
     'belief of': 2019,
     'the directors': 12308,
     'directors of': 3633,
     'the cleveland': 12240,
     'cleveland federal': 2640,
     'reserve bank': 10563,
     'bank that': 1663,
     'the contraction': 12268,
     'contraction will': 3061,
     'will be': 14434,
     'be more': 1797,
     'more prolonged': 7920,
     'prolonged and': 9924,
     'and deeper': 628,
     'deeper than': 3407,
     'than most': 11952,
     'most economists': 7955,
     'economists and': 4024,
     'and public': 820,
     'public policy': 9953,
     'policy makers': 9633,
     'makers are': 7436,
     'are currently': 1139,
     'currently expecting': 3229,
     'these range however': 12981,
     'range however from': 10050,
     'however from the': 5691,
     'from the belief': 4981,
     'the belief that': 12204,
     'belief that the': 2023,
     'that the bottom': 12123,
     'the bottom will': 12218,
     'bottom will come': 2119,
     'will come in': 14448,
     'come in the': 2676,
     'in the third': 6152,
     'the third or': 12765,
     'third or fourth': 13044,
     'or fourth quarter': 9100,
     'fourth quarter of': 4917,
     'quarter of this': 10017,
     'of this year': 8804,
     'this year to': 13116,
     'year to the': 14677,
     'to the belief': 13519,
     'the belief of': 12203,
     'belief of the': 2020,
     'of the directors': 8755,
     'the directors of': 12314,
     'directors of the': 3634,
     'of the cleveland': 8748,
     'the cleveland federal': 12241,
     'cleveland federal reserve': 2641,
     'federal reserve bank': 4531,
     'reserve bank that': 10565,
     'bank that the': 1665,
     'that the contraction': 12124,
     'the contraction will': 12269,
     'contraction will be': 3062,
     'will be more': 14441,
     'be more prolonged': 1799,
     'more prolonged and': 7921,
     'prolonged and deeper': 9925,
     'and deeper than': 629,
     'deeper than most': 3408,
     'than most economists': 11953,
     'most economists and': 7956,
     'economists and public': 4025,
     'and public policy': 821,
     'public policy makers': 9954,
     'policy makers are': 9634,
     'makers are currently': 7437,
     'are currently expecting': 1140,
     'growth in': 5250,
     'in unemployment': 6188,
     'is noticeable': 6692,
     'noticeable throughout': 8300,
     'throughout the': 13174,
     'the country': 12278,
     'country in': 3155,
     'some districts': 11353,
     'districts only': 3818,
     'only mildly': 9031,
     'mildly but': 7765,
     'but in': 2262,
     'in others': 5995,
     'others strongly': 9216,
     'growth in unemployment': 5254,
     'in unemployment is': 6190,
     'unemployment is noticeable': 13809,
     'is noticeable throughout': 6693,
     'noticeable throughout the': 8301,
     'throughout the country': 13175,
     'the country in': 12280,
     'country in some': 3156,
     'in some districts': 6065,
     'some districts only': 11355,
     'districts only mildly': 3819,
     'only mildly but': 9032,
     'mildly but in': 7766,
     'but in others': 2264,
     'in others strongly': 5996,
     'until recently': 13856,
     'recently many': 10215,
     'many firms': 7528,
     'firms were': 4677,
     'were reducing': 14297,
     'reducing their': 10299,
     'their work': 12909,
     'work forces': 14580,
     'forces simply': 4883,
     'simply by': 11191,
     'by letting': 2341,
     'letting attrition': 7131,
     'attrition take': 1565,
     'take its': 11844,
     'its toll': 6849,
     'toll but': 13578,
     'but now': 2267,
     'now firms': 8327,
     'firms are': 4642,
     'are furloughing': 1184,
     'furloughing workers': 5018,
     'workers cutting': 14594,
     'cutting back': 3298,
     'back their': 1630,
     'their staffs': 12903,
     'staffs and': 11526,
     'and pushing': 822,
     'pushing early': 9992,
     'early retirements': 3960,
     'until recently many': 13857,
     'recently many firms': 10216,
     'many firms were': 7531,
     'firms were reducing': 4679,
     'were reducing their': 14298,
     'reducing their work': 10300,
     'their work forces': 12910,
     'work forces simply': 14581,
     'forces simply by': 4884,
     'simply by letting': 11192,
     'by letting attrition': 2342,
     'letting attrition take': 7132,
     'attrition take its': 1566,
     'take its toll': 11845,
     'its toll but': 6851,
     'toll but now': 13579,
     'but now firms': 2268,
     'now firms are': 8328,
     'firms are furloughing': 4645,
     'are furloughing workers': 1185,
     'furloughing workers cutting': 5019,
     'workers cutting back': 14595,
     'cutting back their': 3300,
     'back their staffs': 1633,
     'their staffs and': 12904,
     'staffs and pushing': 11527,
     'and pushing early': 823,
     'pushing early retirements': 9993,
     'in few': 5899,
     'districts even': 3810,
     'even quality': 4218,
     'quality labor': 10002,
     'labor has': 6927,
     'has begun': 5346,
     'begun to': 1975,
     'to be': 13242,
     'be available': 1744,
     'in few districts': 5900,
     'few districts even': 4556,
     'districts even quality': 3811,
     'even quality labor': 4219,
     'quality labor has': 10004,
     'labor has begun': 6929,
     'has begun to': 5347,
     'begun to be': 1976,
     'to be available': 13245,
     'an easier': 512,
     'easier market': 3969,
     'market is': 7584,
     'is noted': 6690,
     'noted for': 8282,
     'for among': 4747,
     'among others': 478,
     'others middle': 9214,
     'middle management': 7755,
     'management and': 7450,
     'and professional': 815,
     'professional types': 9868,
     'types and': 13750,
     'and one': 774,
     'one district': 8985,
     'district remarked': 3770,
     'remarked upon': 10413,
     'upon an': 13889,
     'an extremely': 526,
     'extremely sharp': 4424,
     'sharp increase': 11077,
     'increase in': 6241,
     'in unsolicited': 6191,
     'unsolicited summaries': 13848,
     'summaries from': 11776,
     'from applicants': 4935,
     'applicants with': 1056,
     'with extensive': 14499,
     'extensive experience': 4413,
     'an easier market': 513,
     'easier market is': 3970,
     'market is noted': 7586,
     'is noted for': 6691,
     'noted for among': 8283,
     'for among others': 4748,
     'among others middle': 479,
     'others middle management': 9215,
     'middle management and': 7756,
     'management and professional': 7451,
     'and professional types': 816,
     'professional types and': 9869,
     'types and one': 13751,
     'and one district': 775,
     'one district remarked': 8987,
     'district remarked upon': 3771,
     'remarked upon an': 10414,
     'upon an extremely': 13890,
     'an extremely sharp': 527,
     'extremely sharp increase': 4425,
     'sharp increase in': 11078,
     'increase in unsolicited': 6247,
     'in unsolicited summaries': 6192,
     'unsolicited summaries from': 13849,
     'summaries from applicants': 11777,
     'from applicants with': 4936,
     'applicants with extensive': 1057,
     'with extensive experience': 14500,
     'very few': 13975,
     'few exceptions': 4560,
     'exceptions were': 4272,
     'were noted': 14292,
     'noted to': 8294,
     'the general': 12421,
     'general pattern': 5101,
     'pattern of': 9391,
     'of weakness': 8834,
     'weakness in': 14210,
     'in retail': 6032,
     'retail sales': 10672,
     'sales and': 10795,
     'and of': 771,
     'of downgrading': 8491,
     'very few exceptions': 13976,
     'few exceptions were': 4561,
     'exceptions were noted': 4273,
     'were noted to': 14294,
     'noted to the': 8295,
     'to the general': 13524,
     'the general pattern': 12427,
     'general pattern of': 5102,
     'pattern of weakness': 9392,
     'of weakness in': 8835,
     'weakness in retail': 14213,
     'in retail sales': 6034,
     'retail sales and': 10673,
     'sales and of': 10797,
     'and of downgrading': 773,
     'of downgrading and': 8492,
     'department stores': 3498,
     'stores seemed': 11635,
     'seemed to': 10956,
     'be particularly': 1812,
     'particularly hard': 9367,
     'hard hit': 5314,
     'hit by': 5626,
     'by the': 2387,
     'the softening': 12732,
     'softening of': 11319,
     'of demand': 8469,
     'demand while': 3477,
     'while discount': 14387,
     'discount stores': 3663,
     'stores and': 11619,
     'bargain basements': 1714,
     'basements were': 1730,
     'were holding': 14286,
     'holding up': 5644,
     'up well': 13886,
     'department stores seemed': 3504,
     'stores seemed to': 11636,
     'seemed to be': 10957,
     'to be particularly': 13269,
     'be particularly hard': 1813,
     'particularly hard hit': 9368,
     'hard hit by': 5315,
     'hit by the': 5627,
     'by the softening': 2393,
     'the softening of': 12733,
     'softening of demand': 11320,
     'of demand while': 8471,
     'demand while discount': 3478,
     'while discount stores': 14388,
     'discount stores and': 3664,
     'stores and bargain': 11620,
     'and bargain basements': 583,
     'bargain basements were': 1715,
     'basements were holding': 1731,
     'were holding up': 14287,
     'holding up well': 5646,
     'weakness was': 14216,
     'was particularly': 14148,
     'particularly strong': 9374,
     'strong in': 11699,
     'in furniture': 5904,
     'furniture appliances': 5022,
     'appliances television': 1052,
     'television sets': 11870,
     'sets and': 11024,
     'and clothing': 610,
     'weakness was particularly': 14218,
     'was particularly strong': 14149,
     'particularly strong in': 9375,
     'strong in furniture': 11700,
     'in furniture appliances': 5905,
     'furniture appliances television': 5023,
     'appliances television sets': 1053,
     'television sets and': 11871,
     'sets and clothing': 11025,
     'auto buying': 1571,
     'buying was': 2297,
     'was an': 14101,
     'an area': 508,
     'area where': 1324,
     'where downgrading': 14341,
     'downgrading was': 3906,
     'was especially': 14115,
     'especially intense': 4200,
     'intense except': 6488,
     'except in': 4265,
     'in dallas': 5863,
     'auto buying was': 1572,
     'buying was an': 2298,
     'was an area': 14102,
     'an area where': 509,
     'area where downgrading': 1325,
     'where downgrading was': 14342,
     'downgrading was especially': 3908,
     'was especially intense': 14116,
     'especially intense except': 4201,
     'intense except in': 6489,
     'except in dallas': 4266,
     'the trend': 12777,
     'trend was': 13671,
     'was heavily': 14126,
     'heavily to': 5541,
     'to cheaper': 13296,
     'cheaper models': 2582,
     'models stripped': 7800,
     'stripped down': 11687,
     'down models': 3874,
     'models compacts': 7798,
     'compacts low': 2716,
     'low priced': 7303,
     'priced imports': 9764,
     'imports and': 5771,
     'and late': 732,
     'late model': 7057,
     'model used': 7792,
     'used cars': 13923,
     'the trend was': 12778,
     'trend was heavily': 13672,
     'was heavily to': 14127,
     'heavily to cheaper': 5542,
     'to cheaper models': 13297,
     'cheaper models stripped': 2584,
     'models stripped down': 7801,
     'stripped down models': 11688,
     'down models compacts': 3875,
     'models compacts low': 7799,
     'compacts low priced': 2717,
     'low priced imports': 7304,
     'priced imports and': 9765,
     'imports and late': 5772,
     'and late model': 733,
     'late model used': 7058,
     'model used cars': 7793,
     'outside the': 9291,
     'the auto': 12186,
     'auto field': 1577,
     'field in': 4578,
     'the few': 12391,
     'districts where': 3834,
     'where no': 14347,
     'no downgrading': 8127,
     'was apparent': 14105,
     'apparent consumers': 1014,
     'consumers nevertheless': 2961,
     'nevertheless had': 8073,
     'had sharp': 5289,
     'sharp eye': 11075,
     'eye out': 4426,
     'out for': 9248,
     'for sales': 4835,
     'and specials': 877,
     'outside the auto': 9292,
     'the auto field': 12188,
     'auto field in': 1578,
     'field in the': 4579,
     'in the few': 6112,
     'the few districts': 12392,
     'few districts where': 4559,
     'districts where no': 3835,
     'where no downgrading': 14348,
     'no downgrading was': 8128,
     'downgrading was apparent': 3907,
     'was apparent consumers': 14106,
     'apparent consumers nevertheless': 1015,
     'consumers nevertheless had': 2962,
     'nevertheless had sharp': 8074,
     'had sharp eye': 5290,
     'sharp eye out': 11076,
     'eye out for': 4427,
     'out for sales': 9249,
     'for sales and': 4836,
     'sales and specials': 10799,
     'the san': 12701,
     'san francisco': 10876,
     'francisco district': 4921,
     'district strong': 3786,
     'strong demand': 11695,
     'demand for': 3449,
     'for mobile': 4816,
     'mobile homes': 7788,
     'homes was': 5655,
     'was interpreted': 14134,
     'interpreted as': 6507,
     'as possibly': 1423,
     'possibly form': 9662,
     'form of': 4897,
     'in the san': 6145,
     'the san francisco': 12702,
     'san francisco district': 10877,
     'francisco district strong': 4922,
     'district strong demand': 3787,
     'strong demand for': 11696,
     'demand for mobile': 3457,
     'for mobile homes': 4817,
     'mobile homes was': 7789,
     'homes was interpreted': 5656,
     'was interpreted as': 14135,
     'interpreted as possibly': 6508,
     'as possibly form': 1424,
     'possibly form of': 9663,
     'form of downgrading': 4898,
     'in two': 6183,
     'two districts': 13721,
     'districts richmond': 3824,
     'richmond and': 10722,
     'and st': 878,
     'louis capital': 7295,
     'spending plans': 11481,
     'plans continue': 9554,
     'continue strong': 2994,
     'strong out': 11703,
     'out of': 9254,
     'of fear': 8516,
     'fear of': 4509,
     'of inflation': 8566,
     'inflation or': 6425,
     'or to': 9129,
     'to offset': 13433,
     'offset increased': 8880,
     'increased labor': 6271,
     'labor costs': 6918,
     'in two districts': 6184,
     'two districts richmond': 13722,
     'districts richmond and': 3825,
     'richmond and st': 10723,
     'and st louis': 879,
     'st louis capital': 11506,
     'louis capital spending': 7296,
     'capital spending plans': 2476,
     'spending plans continue': 11483,
     'plans continue strong': 9555,
     'continue strong out': 2995,
     'strong out of': 11704,
     'out of fear': 9255,
     'of fear of': 8517,
     'fear of inflation': 4511,
     'of inflation or': 8571,
     'inflation or to': 6426,
     'or to offset': 9131,
     'to offset increased': 13435,
     'offset increased labor': 8881,
     'increased labor costs': 6272,
     'however in': 5692,
     'the five': 12409,
     'five other': 4706,
     'other districts': 9188,
     'districts that': 3830,
     'that made': 12072,
     'made reference': 7382,
     'reference to': 10317,
     'the subject': 12751,
     'subject many': 11717,
     'are making': 1215,
     'making substantial': 7444,
     'substantial cutbacks': 11731,
     'however in the': 5693,
     'in the five': 6115,
     'the five other': 12410,
     'five other districts': 4707,
     'other districts that': 9189,
     'districts that made': 3831,
     'that made reference': 12073,
     'made reference to': 7383,
     'reference to the': 10318,
     'to the subject': 13528,
     'the subject many': 12752,
     'subject many firms': 11718,
     'many firms are': 7529,
     'firms are making': 4647,
     'are making substantial': 1217,
     'making substantial cutbacks': 7445,
     'among the': 486,
     'the comments': 12246,
     'comments general': 2687,
     'general motors': 5094,
     'motors is': 7994,
     'is making': 6670,
     'making huge': 7438,
     'huge cutbacks': 5716,
     'cutbacks large': 3288,
     'large retail': 7005,
     'retail organization': 10668,
     'organization is': 9164,
     'is cutting': 6610,
     'back by': 1624,
     'by 50': 2305,
     '50 percent': 97,
     'percent large': 9450,
     'large oil': 6999,
     'oil company': 8888,
     'company is': 2746,
     'is continuously': 6606,
     'continuously reviewing': 3055,
     'reviewing its': 10715,
     'its plans': 6837,
     'plans in': 9564,
     'the philadelphia': 12594,
     'philadelphia district': 9507,
     'district there': 3790,
     'there has': 12927,
     'been marked': 1937,
     'marked cutback': 7568,
     'cutback since': 3275,
     'since april': 11193,
     'april and': 1068,
     'the new': 12543,
     'new york': 8104,
     'york district': 14697,
     'district some': 3782,
     'some firms': 11362,
     'are reviewing': 1268,
     'reviewing their': 10717,
     'their plans': 12884,
     'plans for': 9558,
     'for the': 4841,
     'the second': 12708,
     'second or': 10912,
     'or third': 9127,
     'third time': 13045,
     'time this': 13197,
     'among the comments': 487,
     'the comments general': 12247,
     'comments general motors': 2688,
     'general motors is': 5096,
     'motors is making': 7995,
     'is making huge': 6671,
     'making huge cutbacks': 7439,
     'huge cutbacks large': 5718,
     'cutbacks large retail': 3289,
     'large retail organization': 7007,
     'retail organization is': 10669,
     'organization is cutting': 9165,
     'is cutting back': 6611,
     'cutting back by': 3299,
     'back by 50': 1625,
     'by 50 percent': 2306,
     '50 percent large': 98,
     'percent large oil': 9451,
     'large oil company': 7000,
     'oil company is': 8890,
     'company is continuously': 2747,
     'is continuously reviewing': 6607,
     'continuously reviewing its': 3056,
     'reviewing its plans': 10716,
     'its plans in': 6838,
     'plans in the': 9565,
     'in the philadelphia': 6134,
     'the philadelphia district': 12595,
     'philadelphia district there': 9508,
     'district there has': 3791,
     'there has been': 12929,
     'has been marked': 5340,
     'been marked cutback': 1938,
     'marked cutback since': 7570,
     'cutback since april': 3276,
     'since april and': 11194,
     'april and in': 1069,
     'and in the': 717,
     'in the new': 6127,
     'the new york': 12544,
     'new york district': 8108,
     'york district some': 14699,
     'district some firms': 3783,
     'some firms are': 11363,
     'firms are reviewing': 4648,
     'are reviewing their': 1269,
     'reviewing their plans': 10718,
     'their plans for': 12885,
     'plans for the': 9560,
     'for the second': 4856,
     'the second or': 12711,
     'second or third': 10913,
     'or third time': 9128,
     'third time this': 13046,
     'time this year': 13199,
     'inventory holdings': 6536,
     'holdings were': 5649,
     'were specifically': 14313,
     'specifically mentioned': 11461,
     'mentioned by': 7706,
     'by half': 2335,
     'half of': 5293,
     'the districts': 12340,
     'inventory holdings were': 6537,
     'holdings were specifically': 5650,
     'were specifically mentioned': 14314,
     'specifically mentioned by': 11462,
     'mentioned by half': 7708,
     'by half of': 2336,
     'half of the': 5295,
     'of the districts': 8757,
     'they were': 13020,
     'were regarded': 14299,
     'as excessive': 1373,
     'excessive in': 4282,
     'two of': 13736,
     'districts and': 3806,
     'and were': 946,
     'were being': 14268,
     'being reduced': 2007,
     'reduced in': 10267,
     'in third': 6167,
     'they were regarded': 13022,
     'were regarded as': 14300,
     'regarded as excessive': 10337,
     'as excessive in': 1374,
     'excessive in two': 4283,
     'in two of': 6185,
     'two of the': 13737,
     'the districts and': 12341,
     'districts and were': 3807,
     'and were being': 948,
     'were being reduced': 14270,
     'being reduced in': 2009,
     'reduced in third': 10270,
     'two others': 13738,
     'others they': 9217,
     'were at': 14261,
     'at satisfactory': 1516,
     'satisfactory level': 10880,
     'level partly': 7141,
     ...}




```python
tst = word_tokenize(df_fin['text_clean'].iloc[0])
#[tst.remove(stop_words) for stop_words in set(stopwords.words("english")) if stop_words in tst]

for stop_words in list(stopwords.words("english")):
    try: 
        tst.remove(stop_words)
    except: # Do nothing
        continue

token_txt = [word for word in tst if not word in stopwords.words()]
token_txt

def rm_stopwords(text):
    stop_words = set(stopwords.words("english"))
    text_return = text
    for idx, strtxt in enumerate(text):
        if strtxt in stop_words:
            text_return = text_return.replace(strtxt, "")
    return text_return

rm_stopwords(df_fin['text_clean'].iloc[0])

# Tokenize as a whole
#for sentence in df_fin['text']:
#sent_tokenize(df_fin['text'].iloc[0])
#word_tokenize(df_fin['text'].iloc[0])

def preprocess_corpus(texts):
    mystopwords = set(stopwords.words("english"))
    def remove_stops_digits(tokens):
        return [token.lower() for token in tokens if token not in mystopwords or not token.isdigit() and token not in punctuation]
    return [remove_stops_digits(word_tokenize(text)) for text in texts]
preprocess_corpus(df_fin['text'].iloc[0])
```
