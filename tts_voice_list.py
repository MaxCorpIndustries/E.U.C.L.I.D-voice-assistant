import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
voice_num=0
for voice in voices:
    print(voice, voice.id)
    print(voice_num)
    engine.setProperty('voice', voice.id)
    engine.say("Hello World!")
    engine.runAndWait()
    engine.stop()
    voice_num+=1