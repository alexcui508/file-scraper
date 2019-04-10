#!/usr/bin/python
from bs4 import BeautifulSoup
import urllib.request as ureq
import wget
import sys

def download_all(remaining_links, path):
	for link in remaining_links:
		wget.download(link, out=path)

def valid_input(response):
	return response == "y" or response == "n" or response == "d" or response == "q" or response == "yes" or response == "no" or response == "download all" or response == "quit"

URL = 'https://inst.eecs.berkeley.edu/~cs188/fa18/'

# access page html 
opened_page = ureq.urlopen(URL)
page_html = opened_page.read()
opened_page.close()

# parse page html and find all elements belonging to "homeworks" tag
soup = BeautifulSoup(page_html, "html.parser")
weeks = soup.findAll("tbody")

# acquire list of full pdf links
pdf_links = []
print("Retrieving files for cs188...")
for week in weeks:
	a_tags = week.findAll("a")
	for assignment in a_tags:
		if "Section" in assignment.text:
			link = assignment["href"]
			pdf_links.append(URL + link)

# directory that the user downloads file into -- CHANGE TO USER'S DIRECTORY
path = '/Users/alexcui/Desktop/test_folder/'

for link in pdf_links:
	filename = link[59:]	# hardcoded for how cs188 links are styled
	download_method = input("\nConfirm download for " + "\"" + filename + "\"?: [Y]es | [N]o | [D]ownload all | [Q]uit \n").lower()

	while not valid_input(download_method):
		download_method = input("\nError: incorrect format. Please try again\n").lower()

	if download_method == "y" or download_method == "yes":
		wget.download(link, out=path, )
	elif download_method == "n" or download_method == "no":
		continue
	elif download_method == "d" or download_method == "download all":
		print("\nDownloading all scraped files...\n")
		link_index = pdf_links.index(link)
		remaining_links = pdf_links[link_index:]
		download_all(remaining_links, path)
		break
	else:
		sys.exit("Quitting downloads...")
	
print("\nDone")