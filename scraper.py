# -*- coding: utf-8 -*-

import scraperwiki
import urllib2
from datetime import datetime
from bs4 import BeautifulSoup

# Set up variables
entity_id = "E1121_DCC_gov"
url = "http://www.devon.gov.uk/index/councildemocracy/councilfinance/expenditure-over500.htm"

# Set up functions
def convert_mth_strings ( mth_string ):
	month_numbers = {'JAN': '01', 'FEB': '02', 'MAR':'03', 'APR':'04', 'MAY':'05', 'JUN':'06', 'JUL':'07', 'AUG':'08', 'SEP':'09','OCT':'10','NOV':'11','DEC':'12' }
	#loop through the months in our dictionary
	for k, v in month_numbers.items():
		#then replace the word with the number
		mth_string = mth_string.replace(k, v)
	return mth_string

# pull down the content from the webpage
html = urllib2.urlopen(url)
soup = BeautifulSoup(html)

# find all entries with the required class
block = soup.find('div',{'class':'ssp_head'})
links = block.findAll('a', href=True)
	
for link in links:
	url = 'http://www.devon.gov.uk/' + link['href']
	if '.csv' in url:
		#  clean up the onclick data
		title = link.contents[0]
		# create the right strings for the new filename
		csvYr = title.split(' ')[-1]
		csvMth = title.split(' ')[-2][:3]
		csvMth = csvMth.upper()
		csvMth = convert_mth_strings(csvMth);
		filename = entity_id + "_" + csvYr + "_" + csvMth + ".csv"
		todays_date = str(datetime.now())
		scraperwiki.sqlite.save(unique_keys=['l'], data={"l": url, "f": filename, "d": todays_date })
		print filename
