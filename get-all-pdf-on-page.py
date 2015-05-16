"""
A simple command line utility that takes in a list of target url's
and downloads all pdf links contained on the page

Potentially look into using scrapy to build a full fledged crawler instead
"""

import requests
import sys
import re
import subprocess
from bs4 import BeautifulSoup
import urlparse

def process(target_url):
	page = requests.get(target_url)
	print "Succesfully crawled %s" %(target_url)
	print "Searching for pdf links"
	soup = BeautifulSoup(page.text)
	#print soup
	links = soup.findAll(href=re.compile("\.pdf$"))
	for link in links:
		#if pdf is locally linked
		if not link.get('href').startswith("http"): 
			link = urlparse.urljoin(target_url,link.get('href'))
		#if pdf link is absolute
		else:
			link = link.get('href')
		print "Downloading: %s" %(link)
		#Create pdf files
		subprocess.call(["curl", "-O",link],shell=False)
		print "Created: %s" %(link)

def main():
	if len(sys.argv) == 1:
		print "Usage python get-all-pdf-on-page.py target_url_1 target_url_2 ..."
		sys.exit(-1)

	for target_url in sys.argv[1:]:
		process(target_url)

if __name__ == "__main__":
	main()


