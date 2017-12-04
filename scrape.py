
# coding: utf-8

# In[1]:

from bs4 import BeautifulSoup
import urllib
import urllib2
import re

#determine number of pages to scrape links from
url = urllib2.urlopen('https://www.whitehouse.gov/briefing-room/speeches-and-remarks')

content = url.read()
soup = BeautifulSoup(content, "lxml")

number_of_pages = str(soup.find_all('li', class_='pager-current'))
number_of_pages = re.findall(r'\b\d+\b', number_of_pages)[1]

print "Scraping " + str(number_of_pages) + " navigation pages."


# In[2]:

talk_list = {}

pages_to_scrape = []

#change end of range to int(number_of_pages) when wanting to scrape all (that will be a doozy)
for number in range(0,5):
    base = 'https://www.whitehouse.gov/briefing-room/speeches-and-remarks?term_node_tid_depth=31&page='
    page_url = base + str(number)
    
    pages_to_scrape.append(page_url)
    
    
print pages_to_scrape


# In[5]:

for page in pages_to_scrape:
    
    page_url = urllib2.urlopen(page)
    page_content = page_url.read()
    page_soup = BeautifulSoup(page_content, 'lxml')    
            
    for link in page_soup.find_all('h3', class_='field-content'):
        
        if "Vice President" in str(link.contents[0]):
            continue
            
        else:
            rel = str(link.contents[0].get('href'))
            base = 'https://whitehouse.gov'
            talk_list[str(link.contents[0].contents)] = {}
            talk_list[str(link.contents[0].contents)]['url'] = base + rel
            
            #uncomment when updating scraper(otherwise will take forever to update)
            talk_url = urllib2.urlopen(base + rel)
            talk_content = talk_url.read()
            talk_soup = BeautifulSoup(talk_content)
            
            talk = talk_soup.find_all('div', class_='field-items')
            
            talk_list[str(link.contents[0].contents)]['content'] = str(talk)
            
            


# In[7]:

import os, csv
import json

with open('content.csv','w') as toWrite:
    writer = csv.writer(toWrite, delimiter=',')
    writer.writerow(['name','url','content'])
    for a in talk_list.keys():
        writer.writerow([a.encode('utf-8'), talk_list[a]['url'].encode('utf-8'), talk_list[a]['content'].encode('latin-1').decode('utf-8')])

#uncomment when outside firewall
output = open('content.txt','w')

output.write(str(talk_list))

output.close()

