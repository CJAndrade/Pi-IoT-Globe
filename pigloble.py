#!/usr/bin/python
#Create for the for the Pi IoT Globe project posted on instructables.com
#Author : @CarmelitoA 06/23/2017
import RPi.GPIO as GPIO
import time,os,subprocess
import blinkt,colorsys
import weather_condition,traffic_condition,tweets_hashtag
GPIO.setmode(GPIO.BCM)
#tilt sensor connected to pin#20 on the pi zero
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
blinkt.set_clear_on_exit()

while True:
    if ( GPIO.input(20) == False ):
        print("waiting....")
        time.sleep(0.2)
    else:
        print ("Tilt sensor is triggered")
        ##getting weather conidtions from OpenWeatherMap.org - weather_condition.py
        outTemp,outHumidity,outCondition = weather_condition.weatherData()#depending on where you live you can use Temperature or humidity.
        print ("Weather conditions : " + outCondition)
        if outCondition in ('Rain', 'shower rain','thunderstorm'): blinkt.set_all(0, 255, 0) #blue for Rains or thunderstorm
        elif outCondition in ('Clear','Sunny','Few clouds'): blinkt.set_all(255, 255, 0) #yellow
        elif outCondition in ('Mist','Fog'): blinkt.set_all(255, 255, 100) #grey
        else:blinkt.set_all(255, 255, 100) #white if snow, or any other weather conidtion -https://openweathermap.org/weather-conditions
        blinkt.show()
        text = "The Weather conditions currently are " +outCondition + " and the temperature is "+ str(outTemp) + " centigrade and humidity is " + str(outHumidity) + " percent."
        os.system('echo '+text+'|festival --tts')
        time.sleep(1);
        blinkt.set_all(0, 0, 0) #setall LEDs off for 2 seconds
        blinkt.show()
        time.sleep(2);
        ##getting time to work using the Google Maps - Distance Matrix API
        #For me the time to work is ideally 25-30 mins with no traffic
        timeToWork = traffic_condition.get_time_intraffic()
        print ("Time to work :" + str(timeToWork))
        if timeToWork >= 45:  blinkt.set_all(255, 0, 0) # heavy traffic
        elif timeToWork >=30 and timeToWork < 45 : blinkt.set_all(255, 69, 0) #orange some traffic
        else:blinkt.set_all(0, 255, 0) #little traffic <30 mins to work
        blinkt.show()
        text = "And the time to work is " + str(timeToWork) + " minutes "
        os.system('echo '+text+'|festival --tts')
        time.sleep(2)
        blinkt.set_all(0, 0, 0) #setall LEDs off for 2 seconds
        blinkt.show()
        time.sleep(2);

        print ("Tweets for hashtag Raspberry pi zero")
        text = "And here are the tweets for hashtag Raspberry pi zero "
        os.system('echo '+text+'|festival --tts')

        commands = ['festival --tts tweets.txt &', 'sudo python rainbow.py']
        for comm in commands:
            os.system(comm)
