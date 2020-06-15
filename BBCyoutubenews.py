


News_Channel=0
#0 is CNN
#1 is BBC
#2 is UNKNOWN
#3 is UNKNOWN
from datetime import datetime
now = datetime.now()
print(now.strftime("%I"))
current_time = now.strftime("%I:%M %p")
import pyttsx3
engine = pyttsx3.init()
engine.say(current_time)
engine.runAndWait()

url = ("https://www.youtube.com/watch?v=w_Ma8oQLmSM")

video = pafy.new(url)
best = video.getbest()
media = vlc.MediaPlayer(best.url)
media.set_fullscreen(False)
media.video_set_aspect_ratio('16:9')
media.video_set_scale(.5)
media.play()