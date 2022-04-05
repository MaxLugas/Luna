import random
import time
import datetime
import playsound
import os
import re
import webbrowser
import speech_recognition as sr
from gtts import gTTS
import subprocess
import requests
from pyowm import OWM


# import smtplib
# import youtube_dl
# import vlc
# import urllib
# import urllib2
# import json
# from bs4 import BeautifulSoup as soup
# from urllib2 import urlopen
# import wikipedia


# Mетод, который будет интерпретировать голосовой ответ пользователя
#
def listen():
    voice_recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        voice_recognizer.pause_threshold = 1
        voice_recognizer.adjust_for_ambient_noise(source, duration=1)
        print('Say something... ')
        audio = voice_recognizer.listen(source)
    try:
        voice_text = voice_recognizer.recognize_google(audio, language='en')
        print(f'You say: {voice_text}')
        return voice_text
    except sr.UnknownValueError:
        return 'Error'
    except sr.RequestError:
        return 'Error'


# Mетод, который будет проигрывать аудио файл
#
def Luna_say(message):
    voice = gTTS(message)
    audio_file = 'audio.mp3' + str(time.time()) + str(random.randint(1, 10000)) + '.mp3'
    voice.save(audio_file)

    playsound.playsound(audio_file)
    os.remove(audio_file)

    print(f'Luna: {message}')


# Mетод, который будет выпонять команду
#
def handle_command(command):
    command = command.lower()

    # Приветствие и завершение программы
    #
    if command == 'hello':
        now = datetime.datetime.now()
        day_time = int(now.strftime('%H'))
        if day_time < 12:
            Luna_say('Hello Sir. Good morning')
        elif 12 <= day_time < 18:
            Luna_say('Hello Sir. Good afternoon')
        else:
            Luna_say('Hello Sir. Good evening')
    elif command == 'goodbye':
        stop()

    # Сообщить текущее время
    #
    elif 'time' in command:
        now = datetime.datetime.now()
        Luna_say('%d hours %d minutes' % (now.hour, now.minute))

    # Погода в городе
    #
    elif 'current weather' in command:
        reg_ex = re.search('current weather in (.*)', command)
        if reg_ex:
            city = reg_ex.group(1)
            owm = OWM('ab0d5e80e8dafb2cb81fa9e82431c1fa')
            mgr = owm.weather_manager()
            observation = mgr.weather_at_place(city)
            w = observation.weather
            x = w.temperature('celsius')
            Luna_say(
                'The maximum temperature in %s is %0.2f and the minimum temperature is %0.2f degree celcius' % (
                    city, x['temp_max'], x['temp_min']))

    # Рассказывает шутку
    #
    elif 'joke' in command:
        res = requests.get('https://icanhazdadjoke.com/', headers={"Accept": "application/json"})
        if res.status_code == requests.codes.ok:
            Luna_say(str(res.json()['joke']))
        else:
            Luna_say('oops!I ran out of jokes')

    # Открывает тот или иной сайт
    #
    elif 'open' in command:
        reg_ex = re.search('open (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            print(domain)
            url = 'https://www.' + domain
            webbrowser.open(url)
            Luna_say('The website you have requested has been opened for you Sir.')
        else:
            pass

    # Запускает любое приложение с компьютера (пока что работает криво)!!!!!!!!!!!!!!!!!!!
    #
    elif 'launch' in command:
        reg_ex = re.search('launch (.*)', command)
        if reg_ex:
            appname = reg_ex.group(1)
            appname1 = appname + ".exe"
            subprocess.Popen(["open", "-n", "/Applications/" + appname1], stdout=subprocess.PIPE)
            Luna_say('I have launched the desired application')

    else:
        Luna_say('Error, command not found')


# Mетод, выхода из программы
#
def stop():
    Luna_say('Bye bye Sir. Have a nice day')
    exit()


# Mетод, старта программы
#
def start():
    print('Start programm...')

    while True:
        command = listen()
        handle_command(command)


try:
    start()
except KeyboardInterrupt:
    stop()
