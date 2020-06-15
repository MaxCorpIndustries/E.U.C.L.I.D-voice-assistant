import urllib2
import xml.etree.ElementTree
from xml.dom import minidom

def get_element_tree(webaddress):
    response = urllib2.urlopen(webaddress)
    text = response.read()
    root = xml.etree.ElementTree.fromstring(text)
    return root

def get_dom(webaddress):
    text = urllib2.urlopen(webaddress).read()
    dom = minidom.parseString(text)
    return dom

# ******************** Hull Daily Mail *************************

print "From Hull Daily Mail:"

# Using xml.etree.elementtree
print "\nUsing xml.etree.ElementTree:"
hdm_xml = get_element_tree('http://www.hulldailymail.co.uk/hullcity.rss')

headlines = []
stories = []

for child in hdm_xml[0]:
    if child.tag == 'item':
        print child[0].text
        headlines.append(child[0].text)
        stories.append(child[2].text)

# Using minidom
print "\nUsing minidom:"
dom = get_dom('http://www.hulldailymail.co.uk/hullcity.rss')
items = dom.getElementsByTagName('item')

# print items[0].childNodes[1].firstChild.nodeValue <- gets the first title text

for item in items:
    print item.childNodes[1].firstChild.nodeValue

# BBC Hull City Rss Feed

#print "\n\nFrom BBC Hull City RRS Feed:"
#bbc_xml = get_element_tree('http://www.bbc.co.uk/sport/football/teams/hull-city/rss.xml')
#for child in bbc_xml[0]:    
#    if child.tag == 'item':
#        print child[0].text

# Daily mail Hull CIty Feed
print "\n\nFrom The Daily Mail Hull City RSS Feed:"
dm_xml = get_element_tree('http://www.dailymail.co.uk/sport/teampages/hull-city.rss')

dm_titles = []
for child in dm_xml[0]:
    if child.tag == 'item':
        print child[0].text # these may need some leading and trailing characters removed
        dm_titles.append(child[0].text)

