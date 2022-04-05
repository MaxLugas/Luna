import random
import time
import playsound
import os
import re
import webbrowser
import speech_recognition as sr
from gtts import gTTS


# Mетод, который будет интерпретировать голосовой ответ пользователя

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

def Luna_say(message):
    voice = gTTS(message)
    audio_file = 'audio.mp3' + str(time.time()) + str(random.randint(1, 10000)) + '.mp3'
    voice.save(audio_file)

    playsound.playsound(audio_file)
    os.remove(audio_file)

    print(f'Luna: {message}')


# Mетод, который будет выпонять команду

def handle_command(command):
    command = command.lower()

    # Приветствие и завершение программы

    if command == 'hello':
        Luna_say('Hi Max')
    elif command == 'goodbye':
        stop()

    # Открывает тот или иной сайт

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

    else:
        Luna_say('Error, command not found')


# Mетод, выхода из программы

def stop():
    Luna_say('Good bye')
    exit()


# Mетод, старта программы

def start():
    print('Start programm...')

    while True:
        command = listen()
        handle_command(command)


try:
    start()
except KeyboardInterrupt:
    stop()
