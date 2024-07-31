from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import speech_recognition as sr
import pyttsx3

source = r'C:\Users\Kiran\PycharmProjects\ALEXAPROJECT\chromedriver.exe'
service = Service(executable_path=source)
driver = webdriver.Chrome(service=service)


def say(answer):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('volume', 1.0)
    engine.say(answer)
    engine.runAndWait()


r = sr.Recognizer()
audio = None


def listen():
    global audio
    with sr.Microphone() as input:
        print("listening")
        say("listening")
        try:
            audio = r.listen(input, timeout=10, phrase_time_limit=15)
            print("audio captured")
            say("audio captured")
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start.")
            say("listening timed out while waiting for phrase to start.")
def listenexit():
    global audio
    with sr.Microphone() as source:
        print("listening")
        say("listening")
        while True:
            try:
                audio = r.listen(source, timeout=10, phrase_time_limit=15)
                print("audio captured")
                say("audio captured")
                text = r.recognize_google(audio).lower()
                print("You said",text)
                say(text)
                if 'exit' in text:
                    print("exit command received.")
                    say("exit command received")
                    driver.close()  #only closes current tab tab , we can use any of these
                    driver.quit()   #exit entire web browser
                    break
            except sr.UnknownValueError:
                print("i didnt understand")
                say('i didnt understand')

listen()
try:
    if audio:
        print("Recognizing audio")
        answer = r.recognize_google(audio)
        print("Recognized answer",answer)
        say(answer)
        driver.get('https://www.youtube.com/')

        # Wait for the search box to be present
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'search_query'))
        )
        print("Search box located")

        #input to the web
        search_box.send_keys(answer)
        print("Text entered into search box",answer)
        say("Text entered into search box")
        search_box.send_keys(Keys.ENTER)
        print("Search executed")
        say("Search executed")
        #discontinue the browser from exit, by calling listenexit()
        listenexit()

except :
    print("The audio may be not understandable ")





