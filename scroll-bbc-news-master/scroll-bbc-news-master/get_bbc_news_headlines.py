import urllib.request
import xml.etree.ElementTree
import pyttsx3

engine = pyttsx3.init()

print ("News subroutine initiated. News gathered from BBC.")

""" RATE"""
rate = engine.getProperty('rate')   # getting details of current speaking rate
print (rate)                        #printing current voice rate
engine.setProperty('rate', 200)     # setting up new voice rate


"""VOLUME"""
volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
print (volume)                          #printing current volume level
engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1

"""VOICE"""
voices = engine.getProperty('voices')       #getting details of current voice
#engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
engine.setProperty('voice', voices[0].id)   #changing index, changes voices. 1 for female


response = urllib.request.urlopen('http://feeds.bbci.co.uk/news/rss.xml')

text = response.read()

root = xml.etree.ElementTree.fromstring(text)

engine.say(" From BBC news,")
engine.runAndWait()

counter = 0
counter_limit =10

for child in root[0]:
    if child.tag == 'item':

        engine.say("News item number " + str(counter+1))
        engine.runAndWait()

        engine.say(child[0].text + ".")
        engine.runAndWait()
        counter = counter + 1
        if counter == counter_limit: # Break out if we get to ten
            break



