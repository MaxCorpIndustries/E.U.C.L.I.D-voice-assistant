
import requests, json 
  
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
    print(" Temperature is " +
                    str(current_temperature)[:4] + "egrees Celcius \n atmospheric pressure is" +
                    str(current_pressure) + "hPa" +
          "\n humidity is " +
                    str(current_humidiy) +
          "\n  Predictions estamate " +
                    str(weather_description)) 
else: 
    print(" City Not Found ") 