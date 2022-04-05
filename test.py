import random
import time
import playsound
import os
import speech_recognition as sr
from gtts import gTTS
import requests





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

def Luna_say(message):
    voice = gTTS(message)
    audio_file = 'audio.mp3' + str(time.time()) + str(random.randint(1, 10000)) + '.mp3'
    voice.save(audio_file)

    playsound.playsound(audio_file)
    os.remove(audio_file)

    print(f'Luna: {message}')




def handle_command(command):
    command = command.lower()
    if 'joke' in command:
        res = requests.get('https://icanhazdadjoke.com/', headers={"Accept": "application/json"})
        if res.status_code == requests.codes.ok:
            Luna_say(str(res.json()['joke']))
        else:
            Luna_say('oops!I ran out of jokes')


def stop():
    Luna_say('Good bye')
    exit()
def start():
    print('Start programm...')

    while True:
        command = listen()
        handle_command(command)


try:
    start()
except KeyboardInterrupt:
    stop()
