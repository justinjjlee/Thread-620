from bs4 import BeautifulSoup
from urllib.request import urlopen
import re # regular expression
from datetime import datetime

# Data pull -------------------------------------------------------------------
myurl2 = "https://www.federalreserve.gov/monetarypolicy/beigebook202106.htm"
# Pull data
html1 = urlopen(myurl2).read()
soupified = BeautifulSoup(html1, "html.parser")

# Date pull -------------------------------------------------------------------
intro_block = soupified.find("div", {"class": "panel panel-attachments"})
# Pull date and convert to date-time
datereport = re.search('before (.*)\. ', intro_block.get_text())[1];
datereport = datetime.strptime(datereport, '%b %d, %Y')
datereport

# Data pull -------------------------------------------------------------------
# Pull national level data
intro_block.find_next("p")

tst = soupified.find("strong", {"strong": "Overall Economic Activity"})
tst = soupified.find("strong", text="Overall Economic Activity").find_next("p")

tst.get_text()

# Pull each district
district_block = soupified.find("a", {"id": "boston"}).find_next("p")
print(district_block)