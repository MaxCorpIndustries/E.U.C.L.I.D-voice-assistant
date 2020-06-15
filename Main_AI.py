import speech_recognition as sr
import os
import pyttsx3
import wikipedia
engine = pyttsx3.init() # object creation
from gtts import gTTS
import pygame.mixer
from pygame import mixer
import time
import urllib
import requests
import json 
from bs4 import BeautifulSoup
import random
from datetime import datetime
import pafy
import vlc

mixer.init()
##############################################################################################################
                                        #TTS system for variable response#
##############################################################################################################            
""" RATE"""
rate = engine.getProperty('rate')   # getting details of current speaking rate
print (rate)                        #printing current voice rate
engine.setProperty('rate', 170)     # setting up new voice rate


"""VOLUME"""
volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
print (volume)                          #printing current volume level
engine.setProperty('volume',1.5)    # setting up volume level  between 0 and 1

"""VOICE"""
voices = engine.getProperty('voices')       #getting details of current voice
#engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
engine.setProperty('voice', voices[11].id)   #changing index, changes voices. 1 for female
#############################################################################################################

#setup for microphone recognition
r = sr.Recognizer()
m = sr.Microphone()

r.energy_threshold  = 5000

startup=True#if true, this will play the boot up aduio

phraseclock_max=5 #how many times theres no valid input before AI ignores you

random_saying_probability=150 #adds extra chances for a random saying NOT to be said. (less -> more sayings) (0 =100% of the time a saying will play)

#refrences for words of interest to ai
callword = "Euclid"
killword = "nevermind"
openword = "open"
closeword = "close"
newsword = "news"
question_array = ["how","when","why","where","what","who","question"]
action_success=0
action_id=0
selfword = "you"
phraseclock = 0 #if this goes above 3, then euclid will ignore it's attention call
attention=False #if true then ai will responsed to input



#Random_audio_gen = random.randrange(0,5,1)
#print(Random_audio_gen)

##############################################################################################################
                                        #Startup sounds#
########from datetime import datetime###################################################################################################### 
if (startup == True):
    #choose a boot sound - .wav's stored in boot_path
    boot_path = '/home/pi/Glados_AI/GLaDOS/boot_audio/random'

    #required audio:
    os.system('aplay /home/pi/Glados_AI/GLaDOS/boot_audio/required/Announcer-powerupstart.wav')

    time.sleep(1)

    boot_file = os.listdir(boot_path)
    boot_index = random.randrange(0,len(boot_file))
    os.system('aplay ' +boot_path+'/'+boot_file[boot_index])

    #finished powerup
    time.sleep(3)
    os.system('aplay /home/pi/Glados_AI/GLaDOS/boot_audio/required/Announcer-powerupcomplete.wav')
    
##############################################################################################################
                                #AI response to input#
##############################################################################################################            
def AI_response(value):
    print(format(value)) #print speech_rec output
    
    #set the vars this will use to global
    global callword
    global killword
    global openword
    global closeword
    global newsword
    global question_array
    global selfword
    global phraseclock
    global attention
    global action_success
    global action_id

    #checks if the callword was spoken
    if (callword in value):
        if (attention == False):
            print("     ATTENTION GAINED")
            phraseclock=0
            attention=True #set alertness to true
        if (len(value) == 6):
            #choose a response sound - .wav's stored in howy_path
            hello_path = '/home/pi/Glados_AI/GLaDOS/hello'
            hello_file = os.listdir(hello_path)
            hello_index = random.randrange(0,len(hello_file))
            os.system('aplay ' +hello_path+'/'+hello_file[hello_index])        
        

    #checks if the killword was spoken
    if (killword in value) and (attention == True):
        print("     ATTENTION LOST")
        attention=False #set alertness to true
        phraseclock=0 #Reset counter
        
        random_saying()  #initialize a random statement
    
    
    #detecting if a question was asked
    if (attention == True): 
         for x in range(len(question_array)): #check to see if what,when,where,why,how and who were said
            if (question_array[x] in value): #if true, question detected.
                if ('weather' in value): #check if the question is about news
                    weather_data()#open the weather
                else:
                    if ('news' in value): #check if the question is about news
                        news_live()#open the news
                    else:
                        if ('time' in value): #check if the question is about time
                            time() #run time method
                        else:
                            if (selfword in value): #check if the question is about itself (look for 'you')
                                if (x==0): #"How are you?"
                                    #choose a response sound - .wav's stored in howy_path
                                    howy_path = '/home/pi/Glados_AI/GLaDOS/you/Howareyou'
                                    howy_file = os.listdir(howy_path)
                                    howy_index = random.randrange(0,len(howy_file))
                                    os.system('aplay ' +howy_path+'/'+howy_file[howy_index])
                                    
                                if (x==4) or (x==5): #"Who are you?"
                                    os.system('aplay /home/pi/Glados_AI/GLaDOS/you/whoareyou/GLaDOS-ID1.wav')
                                    os.system('aplay /home/pi/Glados_AI/GLaDOS/you/whoareyou/GLaDOS-ID2.wav')
                            else:
                                
                                #choose a response sound - .wav's stored in qresp_path
                                qresp_path = '/home/pi/Glados_AI/GLaDOS/response/questions/random'
                                qresp_file = os.listdir(qresp_path)
                                qresp_index = random.randrange(0,len(qresp_file))
                                os.system('aplay ' +qresp_path+'/'+qresp_file[qresp_index])                
                                
                                os.system('aplay /home/pi/Glados_AI/GLaDOS/response/questions/required/GLaDOS-usefulquestion.wav')
                                
                                question_retrival(value) #send question to question retrival
def time():
        #choose a response sound - .wav's stored in qresp_path
    time_path = '/home/pi/Glados_AI/GLaDOS/time/snarky'
    time_file = os.listdir(time_path)
    time_index = random.randrange(0,len(time_file))
    os.system('aplay ' +time_path+'/'+time_file[time_index])                
    
    os.system('aplay /home/pi/Glados_AI/GLaDOS/time/GLaDOS-actualtime.wav')
    now = datetime.now()
    for x in range(1,59):
        if (x-int(now.strftime("%I")) ==0):
            os.system('aplay /home/pi/Glados_AI/GLaDOS/numbers/GLaDOS-'+str(x)+'.wav')
            
        if (x-int(now.strftime("%M")) ==0):
            os.system('aplay /home/pi/Glados_AI/GLaDOS/numbers/GLaDOS-'+str(x)+'.wav')
            
    if ('PM' == now.strftime("%p")):
        os.system('aplay /home/pi/Glados_AI/GLaDOS/time/ampm/GLaDOS-PM.wav')
    if ('AM' == now.strftime("%p")):
        os.system('aplay /h1ome/pi/Glados_AI/GLaDOS/time/ampm/GLaDOS-AM.wav')            
        

##############################################################################################################
                                        #Random Saying system#
############################################################################################################## 
def random_saying():
    
    global random_saying_probability
    #choose an error comment sound - .wav's stored in err_path
    say_path = '/home/pi/Glados_AI/GLaDOS/randomsayings'
    say_file = os.listdir(say_path)
    try:
        say_index = random.randrange(0,len(say_file)+random_saying_probability)
        os.system('aplay ' +say_path+'/'+say_file[say_index]) 
    except IndexError:
        print('random saying failed' + ' | (current:' +str(say_index) + '| first 9 are valid )')
        pass
def news_live():
    News_Channel=0
    #0 is CNN
    #1 is BBC
    #2 is UNKNOWN
    #3 is UNKNOWN

    url = ("https://www.youtube.com/watch?v=w_Ma8oQLmSM")

    video = pafy.new(url)
    best = video.getbest()
    media = vlc.MediaPlayer(best.url)
    media.set_fullscreen(False)
    media.video_set_aspect_ratio('16:9')
    media.video_set_scale(.5)
    media.play()
    while True:
        print("Input_interrupt?")
        with m as source: audio = r.listen(source)
        print("..Processing..")
        try:
            # recognize speech using Google Speech Recognition
            value = r.recognize_google(audio)

            # we need some special handling here to correctly print unicode characters to standard output
            if str is bytes:  # this version of Python uses bytes for strings (Python 2)
                print(format(value).encode("utf-8"))
            else:
                print(value)
                if ("stop" in value) or ("Euclid" in value) or ("cancel" in value)or ("euclid" in value)or ("close" in value):
                    media.stop()
                    action_success=3
                    print("INTERUUPT!")
                    return
                
        except sr.UnknownValueError:
            print("Audio was not understood.")
        except sr.RequestError as e:
            print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))    
##############################################################################################################
                                        #Weather#
############################################################################################################## 
def weather_data():
      
    api_key = "d8946fa50d02dac6a2cf919498ff51ee"

    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    city_name = 'Durham'
    print(city_name)
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name 
    response = requests.get(complete_url)  
    x = response.json()   
    if x["cod"] != "404": 
        y = x["main"] 
        current_temperature = y["temp"]-273
        current_pressure = y["pressure"] 
        current_humidiy = y["humidity"] 
        z = x["weather"] 
        weather_description = z[0]["description"]
        tts=gTTS( "In the city of "+ city_name +", Temperature is " +
                    str(current_temperature)[:4] + "degrees Celcius \n atmospheric pressure is" +
                    str(current_pressure) + "hPa" +
          "\n humidity is " +
                    str(current_humidiy) +
          "\n  Predictions estamate " +
                    str(weather_description))
        print( "In the city of "+ city_name +", Temperature is " +
                    str(current_temperature)[:4] + "degrees Celcius \n atmospheric pressure is" +
                    str(current_pressure) + "hPa" +
          "\n humidity is " +
                    str(current_humidiy) +
          "\n  Predictions estamate " +
                    str(weather_description))
        tts.save('/home/pi/Glados_AI/GLaDOS/question_ai/answer.mp3')
        mixer.music.load('/home/pi/Glados_AI/GLaDOS/question_ai/answer.mp3')
        mixer.music.play()
    else: 
        print(" City Not Found ")
##############################################################################################################
                                        #Question and Answer system#
############################################################################################################## 
def question_retrival(value):
    global action_success
    global action_id
    action_id=1
    mixer.music.load('/home/pi/Glados_AI/GLaDOS/question_ai/1.mp3') #Aperture Science useless question construct is now online.
    mixer.music.play()
    while (pygame.mixer.music.get_busy() == True):
        x=0
        x=x                
    waiting=0
    for i in range(0,1000):
        i=i
    question_approved=False#is true when the quora page for the question exists.
    query=value
    query = query.replace(' ', '-')
    #getting rid of callsign
    query = query.replace('Hey-', '')
    query = query.replace('hey-', '')
    query = query.replace('euclid-', '')
    query = query.replace('Euclid-', '')
    query = query.replace('-euclid', '')
    query = query.replace('-Euclid', '')
    query = query.replace('-euclid-', '')
    query = query.replace('-Euclid-', '')
        
    query = query.replace('question-', '')
    query = query.replace('Question-', '')

    URL = f"https://www.quora.com/{query}"
    print(URL)
    
    # desktop user-agent
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    # mobile user-agent
    MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"

    headers = {"user-agent" : MOBILE_USER_AGENT}
    resp = requests.get(URL, headers=headers)

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")
        
        mixer.music.load('/home/pi/Glados_AI/GLaDOS/question_ai/3.mp3') #Potential answer detected. Initiating interrogation of human child.
        mixer.music.play()
        while (pygame.mixer.music.get_busy() == True):
            x=0
            x=x            
        print("Page exists. Scraping info")
        question_approved = True
    else:
        
        mixer.music.load('/home/pi/Glados_AI/GLaDOS/question_ai/4.mp3') #Error. Unable to locate living specimin for answer. 
        mixer.music.play()
        while (pygame.mixer.music.get_busy() == True):
            x=0
            x=x            
        print("Page does not exist.")
        question_approved = False
        
    title = ""
    title_img = ""

    if (question_approved == True):
        
        for g in soup.find_all('div', class_='ui_qtext_truncated_text'):
            try:
                title = g.find('p').text
            except AttributeError:
                print("[ans cannot be found in P class, switching to backup SPAN class.]")
            
        if (title == ''):
            for g in soup.find_all('div', class_='ui_qtext_expanded'):
                try:
                    title = g.find('span').text
                except AttributeError:
                    print("[ans cannot be found in SPAN class, trying a new div]")    

        if (title == ''):
            for g in soup.find_all('div', class_='ui_qtext_truncated ui_qtext_truncated_regular'):
                try:
                    title = g.find('span').text
                except AttributeError:
                    print("[ans cannot be found in SPAN class]")    

        mixer.music.load('/home/pi/Glados_AI/GLaDOS/question_ai/5.mp3') #Interrogation successful. Answer located.
        mixer.music.play()
        while (pygame.mixer.music.get_busy() == True):
            x=0
            x=x
        print(title)
        tts=gTTS(title,lang='en')
        tts.save('/home/pi/Glados_AI/GLaDOS/question_ai/answer.mp3')
        
        mixer.music.load('/home/pi/Glados_AI/GLaDOS/question_ai/answer.mp3')
        mixer.music.play()

        #with m as source: r.adjust_for_ambient_noise(source)
        while (pygame.mixer.music.get_busy() == True):
            print("Input_interrupt?")
            with m as source: audio = r.listen(source)
            print("..Processing..")
            try:
                # recognize speech using Google Speech Recognition
                value = r.recognize_google(audio)

                # we need some special handling here to correctly print unicode characters to standard output
                if str is bytes:  # this version of Python uses bytes for strings (Python 2)
                    print(format(value).encode("utf-8"))
                else:
                    print(value)
                    if ("stop" in value) or ("Euclid" in value) or ("cancel" in value)or ("euclid" in value):
                       mixer.music.load('/home/pi/Glados_AI/GLaDOS/question_ai/interrupt.mp3')
                       mixer.music.play()
                       action_success=3
                       print("INTERUUPT!")
                       return
                    
            except sr.UnknownValueError:
                print("Audio was not understood.")
            except sr.RequestError as e:
                print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))    
        action_success=1
    else:
        mixer.music.load('/home/pi/Glados_AI/GLaDOS/question_ai/6.mp3')#Attempt to gather information from human child has failed. Accessing wikipedia.
        mixer.music.play()
        while (pygame.mixer.music.get_busy() == True):
            x=0
            x=x          
        #filter out random info
        query = query.replace('what', '')
        query = query.replace('when', '')
        query = query.replace('where', '')
        query = query.replace('how', '')
        query = query.replace('why', '')
        query = query.replace('who', '')
        
        query = query.replace('What', '')
        query = query.replace('When', '')
        query = query.replace('Where', '')
        query = query.replace('How', '')
        query = query.replace('Why', '')
        query = query.replace('Who', '')
        
        query = query.replace('-is-', '')
        query = query.replace('-it-', '')
        query = query.replace('-the-', '')
        query = query.replace('-was-', '')
        query = query.replace('-a-', '')
        query = query.replace('-an-', '')
        
        query = query.replace('---', ' ')
        query = query.replace('--', ' ')
        query = query.replace('-', ' ')
        print(query)
        try:
            wikipedia.search(query, results=10, suggestion=False)
        except wikipedia.exceptions.PageError:
            mixer.music.load('/home/pi/Glados_AI/GLaDOS/question_ai/7.mp3')#Error. Wikipedia has no relevant information to your question. Suicide engaged.
            mixer.music.play()
            while (pygame.mixer.music.get_busy() == True):
                x=0
                x=x            
            print('no wikipedia page found.')
            action_success=2
            return
        
        mixer.music.load('/home/pi/Glados_AI/GLaDOS/question_ai/8.mp3') #Wikipedia article found.
        mixer.music.play()
        while (pygame.mixer.music.get_busy() == True):
            x=0
            x=x            
        engine.say(wikipedia.summary(query,sentences=3))
        print(wikipedia.summary(query))
        
        tts=gTTS(wikipedia.summary(query),lang='en')
        tts.save('/home/pi/Glados_AI/GLaDOS/question_ai/answer.mp3')
        mixer.music.load('/home/pi/Glados_AI/GLaDOS/question_ai/answer.mp3')
        mixer.music.play()
        #with m as source: r.adjust_for_ambient_noise(source)
        
        while (pygame.mixer.music.get_busy() == True):
            print("Input_interrupt?")
            with m as source: audio = r.listen(source)
            print("..Processing..")
            try:
                # recognize speech using Google Speech Recognition
                value = r.recognize_google(audio)

                # we need some special handling here to correctly print unicode characters to standard output
                if str is bytes:  # this version of Python uses bytes for strings (Python 2)
                    print(format(value).encode("utf-8"))
                else:
                    print(value)
                    if ("stop" in value) or ("Euclid" in value) or ("cancel" in value)or ("euclid" in value):
                       mixer.music.load('/home/pi/Glados_AI/GLaDOS/question_ai/interrupt.mp3')
                       mixer.music.play()
                       action_success=3
                       print("INTERUUPT!")
                       return
            except sr.UnknownValueError:
                print("Audio was not understood.")
            except sr.RequestError as e:
                print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
        action_success=1                
               

##############################################################################################################
                                        #User voice recognition#
##############################################################################################################            

def threshold_reset():
    r.energy_threshold=5000

try:
    print("EUCLID Voice response booting...")
    #with m as source: r.adjust_for_ambient_noise(source)
    print("Set minimum energy threshold to {}".format(r.energy_threshold))
    while True:
        threshold_reset()
        print("Input? :{}".format(r.energy_threshold))
        with m as source: audio = r.listen(source)
        print("..Processing..")
        try:
                # recognize speech using Google Speech Recognition
            value = r.recognize_google(audio)
            # we need some special handling here to correctly print unicode characters to standard output
            if str is bytes:  #this version of Python uses bytes for strings (Python 2)
                print(format(value).encode("utf-8"))
            else:       
                AI_response(value)
            
##############################################################################################################
                                #AI reponse of action status#
##############################################################################################################                 
            
            #responds if action failed
            if (action_success==2):
                #if no action was performed -prob an error
                if(action_id==0):
                    action_success=0
                else:            
                     #choose an error comment sound - .wav's stored in err_path
                    err_path = '/home/pi/Glados_AI/GLaDOS/errors'
                    err_file = os.listdir(err_path)
                    err_index = random.randrange(0,len(err_file))
                    os.system('aplay ' +err_path+'/'+err_file[err_index])                        
            #responds if the action worked
            if(action_success==1):
                if(action_id ==1): #question mode
                    os.system('aplay /home/pi/Glados_AI/GLaDOS/response/questions/required/GLaDOS-questionend.wav')
                    
            #responds if the action was interuptted
            if(action_success==3):
                if(action_id ==1): #question mode
                    os.system('aplay /home/pi/Glados_AI/GLaDOS/response/questions/required/GLaDOS-questioninteruppted.wav')
                    
            #wipe action history.
            action_success=0
            action_id=0                 

        except sr.UnknownValueError:
            print("Audio was not understood.")
        except sr.RequestError as e:
            print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
            
        #this phraseclock enables and disables attention mode after serveral non callword/killword phrases
        if (phraseclock < phraseclock_max):
            phraseclock+=1
        else:
            print("     ATTENTION LOST")
            attention=False
            phraseclock=0 #Reset counter
            random_saying() #initialize a random statement                        
except KeyboardInterrupt:
    pass


