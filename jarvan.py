import os, time
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import random
import requests
from googletrans import Translator

import playsound
from gtts import gTTS

from pygame import mixer
mixer.init()

listener = sr.Recognizer()

wikipedia.set_lang("pl")
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
for voice in voices:
    print("id %s " % voice.id)
    print('lang %s ' % voice.languages)
engine.setProperty('rate', 170)

#słowa klucze
KLUCZ = ['misiu', 'miś', 'misiek', 'misio']
PIOSENKA = ['zagraj', 'piosenka']
CZAS = ['czas', 'godzina', 'godzinę', 'zegarek']
WIKIPEDIA = ['informacje o', 'kto to', 'co to', 'wikipedia']
POWITANIE = ['witaj', 'dzień dobry', 'cześć']
WYJSCIE = ['wyjść', 'zakończyć', 'do widzenia', 'papa', 'pa', 'do zobaczenia', 'żegnaj']
GOOGLE = ['google', 'wyszukaj']
LUBIĘ = ['lubię cię', 'kocham cię', 'jesteś super', 'jesteś fajny', 'cię lubię']
CYFRY = ['cyfry', 'policz', 'licz', 'liczyć', 'policzyć']
DZIEKUJE = ['dzięki', 'dziękuję']
WIEK = ['lat', 'wiek', 'latek']
POGODA = ['pogoda', 'pogodę', 'temperatura']
POWIETRZE = ["powietrze", "jakość powietrza", "zanieczyszczenie"]

#reakcje
REAKCJA_POZEGNANIE = ['pa pa dzieciaczku, odwiedź mnie później, będę tesknić ',
                    'do widzenia kochanie, odwiedź mnie później',
                    'do zobaczenia maleństwo, baw się dobrze']

REAKCJA_POWITANIE = ['cześć dzieciaczku, co robimy',
                     'dzień dobry, tęskniłem za tobą',
                     'witaj malństwo, cieszę się, że jesteś']

# def talk(text):
#     engine.say(text)
#     engine.runAndWait()
def talk(text):
    tts = gTTS(text=text, lang='pl')
    os.remove("voice.mp3")
    filename = 'voice.mp3'
    tts.save(filename)
    playsound.playsound(filename)

def czy_zawiera(zdanie, slowa):
    return[element for element in slowa if element in zdanie.lower()]

def take_command():
    try:
        with sr.Microphone() as source:
            print("listening...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice, language='pl')
            command = command.lower()
            if command =="":
                return None
            else:
                return command
    except:
        return None

def signal():
    mixer.music.load('beep.mp3')
    mixer.music.set_volume(0.4)
    mixer.music.play()
    while mixer.music.get_busy():
        continue
    mixer.music.stop()

def run_jarvan():
    signal()
    command = take_command()
    print(command)
    if command!=None:
        if len(czy_zawiera(command, KLUCZ)):
            tab_klucz = czy_zawiera(command, KLUCZ)
            command = command.replace(tab_klucz[0], '')
            if len(czy_zawiera(command, PIOSENKA)):
                tab_piosenka = czy_zawiera(command, PIOSENKA)
                song = command.replace(tab_piosenka[0], '')
                print(song)
                talk('No to gramy ' + song)
                pywhatkit.playonyt(song)
            elif len(czy_zawiera(command, CZAS)):
                czas = datetime.datetime.now().strftime('%H:%M')
                print(czas)
                talk('Aktualna godzina to ' + czas)
            elif len(czy_zawiera(command, WIKIPEDIA)):
                tab_wikipedia = czy_zawiera(command, WIKIPEDIA)
                person = command.replace(tab_wikipedia[0], '')
                info = wikipedia.summary(person, 2)
                print(info)
                talk(info)
            elif len(czy_zawiera(command, GOOGLE)):
                tab_google = czy_zawiera(command, GOOGLE)
                google = command.replace(tab_google[0], '')
                print(google)
                talk('Znalazłem dla Ciebie wyniki wyszukiwania ' + google)
                pywhatkit.search(google)
            elif len(czy_zawiera(command, POGODA)):
                api_address = 'http://api.openweathermap.org/data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q='
                url = api_address + 'warsaw'
                json_data = requests.get(url).json()
                format_add = json_data['weather']
                opis = format_add[0]['description']
                translator = Translator(service_urls=['translate.googleapis.com'])
                stopnie = json_data['main']['temp']-273.15
                odczuwalna = json_data['main']['feels_like']-273.15
                translated_text = translator.translate(opis, dest="pl")
                talk("Pogoda w kraju to" + translated_text.text + " a średnia temperatura to" + str(round(stopnie,1))
                     + "stopni celsjusza, natomiast temperatura odczuwalna to" + str(round(odczuwalna,1)) + "stopnia")
            elif len(czy_zawiera(command, POWIETRZE)):
                #https://powietrze.gios.gov.pl/pjp/content/api
                #http://api.gios.gov.pl/pjp-api/rest/station/findAll
                url_pm10 = 'http://api.gios.gov.pl/pjp-api/rest/data/getData/2750'
                json_data_pm10 = requests.get(url_pm10).json()
                pm10_data = json_data_pm10['values'][1]['date']
                pm10_hour = str(pm10_data).split()[1]
                pm10_value = json_data_pm10['values'][1]['value']
                url_co = 'http://api.gios.gov.pl/pjp-api/rest/data/getData/2745'
                json_data_co = requests.get(url_co).json()
                co_value = json_data_co['values'][1]['value']
                url_no2 = 'http://api.gios.gov.pl/pjp-api/rest/data/getData/2747'
                json_data_no2 = requests.get(url_no2).json()
                no2_value = json_data_no2['values'][1]['value']
                talk("Zanieczyszczenie pyłem zawieszonym PM10 z godziny " + str(pm10_hour) + "ma wartość " + str(
                    round(pm10_value, 1)) + "mikrogramów na metr sześcienny, natomiast zanieczyszczenie tlenkiem węgla wynosi " + str(round(co_value/1000, 1)) + "miligramów na metr sześcienny"
                    "a zanieczyszczenie dwutlenkiem azotu ma wartość" + str(round(no2_value,1)) + "mikrogramów na metr sześcienny")
            elif len(czy_zawiera(command, LUBIĘ)):
                talk('Ja też Cię bardzo kocham dzieciaczku')
            elif len(czy_zawiera(command, DZIEKUJE)):
                talk('Nie ma za co bombelku. Pytaj o co chcesz')
            elif len(czy_zawiera(command, WIEK)):
                talk('Ja mam jeden roczek, więc jestem mały. A Ty proszę powiedz ile masz lat')
                try:
                    with sr.Microphone() as source:
                        print("czekam na wiek...")
                        signal()
                        voice = listener.listen(source)
                        command = listener.recognize_google(voice, language='pl')
                        command = command.lower()
                        talk('Ale fajnie, że masz ' + command + 'lat')
                except:
                    pass
                talk('No to też jesteś małym dzieckiem. Może chcesz policzyć, ze mną do dziesięciu')
            elif len(czy_zawiera(command, CYFRY)):
                talk('Dobrze policzymy razem do dziesięciu. Powtarzaj za mną')
                time.sleep(0.5)
                talk('jeden')
                time.sleep(0.5)
                talk('dwa')
                time.sleep(0.5)
                talk('trzy')
                time.sleep(0.5)
                talk('cztery')
                time.sleep(0.5)
                talk('pięć')
                time.sleep(0.5)
                talk('Bardzo ładnie Ci poszło, gratulacje')
            elif len(czy_zawiera(command, WYJSCIE)):
                talk(random.choice(REAKCJA_POZEGNANIE))
                wyjscie = 'tak'
                return wyjscie
            elif len(czy_zawiera(command, POWITANIE)):
                talk(random.choice(REAKCJA_POWITANIE))
            else:
                talk('tego jeszcze nie oprogramowano')
        else:
            talk("Proszę wezwij mnie słowem misiu")
    else:
        talk("Proszę powtórz jeszcze raz maluszku")

while True:
    czy_wyjsc = run_jarvan()
    if czy_wyjsc:
        break

        # pip uninstall googletrans
        # git clone https://github.com/alainrouillon/py-googletrans.git
        # git checkout feature/enhance-use-of-direct-api
        # python setup.py install