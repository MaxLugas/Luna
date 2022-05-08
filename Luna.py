import random
import time
import datetime
import playsound2
import os
import re
import webbrowser
import speech_recognition as sr
from gtts import gTTS
import requests
from pyowm import OWM


# Mетод, который будет интерпретировать голосовой ответ пользователя
#
def listen():
    voice_recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        voice_recognizer.pause_threshold = 1
        voice_recognizer.adjust_for_ambient_noise(source, duration=1)
        Luna_say('What is your command? ')
        audio = voice_recognizer.listen(source)
    try:
        voice_text = voice_recognizer.recognize_google(audio, language='en')
        print(f'You say: {voice_text}')
        return voice_text
    except sr.UnknownValueError:
        return 'Error'
    except sr.RequestError:
        return 'Error'


def silence():
    voice_recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        voice_recognizer.pause_threshold = 1
        voice_recognizer.adjust_for_ambient_noise(source, duration=1)
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

    playsound2.playsound(audio_file)
    os.remove(audio_file)

    print(f'Luna: {message}')


# Mетод, который будет выпонять команду
#
def handle_command(command):
    command = command.lower()

    # Функции для выхода из программы
    #
    if command == 'bye' or command == 'goodbye' or command == 'stop program':
        stop()

    # Узнать функционал помощника
    #
    elif 'help' in command:
        Luna_say(
            "If you want to know the current time, tell me the time. "
            "If you want to get a weather forecast, say weather and add the city you want to know about. "
            "If you want me to tell a joke, then tell a joke. "
            "If you need to open a website, then tell me to open the name of the website with the domain. "
            "If you need help with the choice, then tell me the choice. "
            "If you don't know what to watch, then tell me the movie")


    # Сообщить текущее время
    #
    elif 'time' in command:
        now = datetime.datetime.now()
        Luna_say('%d hours %d minutes' % (now.hour, now.minute))

    # Погода в городе
    #
    elif 'weather' in command:
        reg_ex = re.search('weather in (.*)', command)
        if reg_ex:
            city = reg_ex.group(1)
            owm = OWM('ab0d5e80e8dafb2cb81fa9e82431c1fa')
            mgr = owm.weather_manager()
            observation = mgr.weather_at_place(city)
            w = observation.weather
            x = w.temperature('celsius')
            Luna_say(
                'The maximum temperature in %s is %0.2f and the minimum is %0.2f degree celcius' % (
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
            Luna_say('I opened the site in your browser')
        else:
            pass

    # Магический шар
    #
    elif 'choice' in command:
        answer = ["Indisputably", "Predetermined", "No doubt", "Definitely yes", "You can be sure of it",
                  "It seems to me - yes", "Most likely", "Good prospects", "Signs say - yes", "Yes",
                  "It's not clear yet, try again", "Ask later", "It's better not to tell",
                  "It's impossible to predict now",
                  "Concentrate and ask again", "Don't even think", "My answer is no", "According to my data - no",
                  "The prospects are not very good", "Very doubtful"]
        Luna_say('What is your question?')
        command = silence()
        Luna_say(random.choice(answer))
        Luna_say('Are you have any question?')
        command = silence()
        command = command.lower()
        while command == 'yes':
            Luna_say('What is your question?')
            command = silence()
            Luna_say(random.choice(answer))
            Luna_say('Are you have any question?')
            command = silence()
            command = command.lower()

    # Подбор фильмов
    #
    elif 'film' in command:
        Luna_say('What style of film you want to see? I have three positions: horror, comedy and cartoon')
        command = silence()
        if command == 'horror':
            n = random.randint(1, 100)
            with open('horror.txt') as file:
                for index, line in enumerate(file):
                    if index == n - 1:
                        Luna_say(line)
                        break
        elif command == 'comedy':
            n = random.randint(1, 100)
            with open('comedy.txt') as file:
                for index, line in enumerate(file):
                    if index == n - 1:
                        Luna_say(line)
                        break
        elif command == 'cartoon':
            n = random.randint(1, 50)
            with open('cartoon.txt') as file:
                for index, line in enumerate(file):
                    if index == n - 1:
                        Luna_say(line)
                        break

    else:
        Luna_say('Error, command not found')


# Mетод, выхода из программы
#
def stop():
    Luna_say('Bye')
    exit()


# Mетод, старта программы
#
def start():
    print('Start programm...')
    now = datetime.datetime.now()
    day_time = int(now.strftime('%H'))
    Assistant = ("I'm your personal voice assistant, if you need to know my functions say help")
    if day_time < 12:
        Luna_say('Good morning,' + Assistant)
    elif 12 <= day_time < 18:
        Luna_say('Good afternoon,' + Assistant)
    else:
        Luna_say('Good evening,' + Assistant)

    while True:
        command = listen()
        handle_command(command)


try:
    start()
except KeyboardInterrupt:
    stop()
