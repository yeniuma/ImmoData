from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import speech_recognition as sr
import requests
import soundfile
import re

page = "https://www.immobilienscout24.de/Suche/at/wien/wien/wohnung-mieten?pricetype=rentpermonth&enteredFrom=result_list"
nums = {'null': '0', 'ein': '1', 'zwei': '2', 'drei': '3', 'vier': '4', 'fünf': '5', 'sechs': '6', 'sieben': '7', 'acht': '8', 'neun': '9'}

service_path = Service(executable_path="F:/ChromeDriver/chromedriver.exe")
options = Options()
driver = webdriver.Chrome(service=service_path, options=options)
driver.get(page)

def save_captcha_audio(driver, path, try_again=False):
    if try_again:
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,"geetest_refresh"))).click()
    else:
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,"geetest_radar_tip"))).click()
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,"geetest_voice"))).click()
    time.sleep(10)
    audio_src = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,"geetest_music"))).get_attribute('src')
    content = requests.get(audio_src).content
    open(path +'/captcha_file.wav', 'wb').write(content)
    data, samplerate = soundfile.read(path + '/captcha_file.wav')
    soundfile.write(path + '/captcha_file_new.wav', data, samplerate, subtype='PCM_16')


def transcribe_audio_file(driver, captcha_source):
    r = sr.Recognizer()
    captcha_not_solved = True
    while captcha_not_solved:
        with sr.AudioFile(captcha_source) as source:
            audio = r.listen(source)
            try:
                text = r.recognize_vosk(audio,language='de').replace('geben sie ein was sie hören','')
                for key, value in nums.items():
                    text = text.replace(key, value)
                text = text.replace(' ','')
                text = re.findall('[0-9]+',text)[0]
                driver.find_element(by=By.CLASS_NAME,value='geetest_input').clear()
                driver.find_element(by=By.CLASS_NAME,value='geetest_input').click()
                time.sleep(3)
                driver.find_element(by=By.CLASS_NAME,value='geetest_input').send_keys(text)
                WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CLASS_NAME,"geetest_submit"))).click()
                if driver.find_element(by=By.CLASS_NAME,value="geetest_result_tip").is_displayed():
                    save_captcha_audio(driver, try_again=True)
                    continue
                captcha_not_solved = False
                time.sleep(15)
            except sr.UnknownValueError:
                save_captcha_audio(driver, try_again=True)

save_captcha_audio(driver,'F:/ImmoData/audio')
transcribe_audio_file(driver,'F:/ImmoData/audio/captcha_file_new.wav')
