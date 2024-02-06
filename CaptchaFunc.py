from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import time
import speech_recognition as sr
import requests
import soundfile
import re


nums = {
    "null": "0",
    "ein": "1",
    "zwei": "2",
    "drei": "3",
    "vier": "4",
    "fünf": "5",
    "sechs": "6",
    "sieben": "7",
    "acht": "8",
    "neun": "9",
}


def check_if_captcha_page(driver):
    if len(driver.find_elements(By.CLASS_NAME, "geetest_radar_tip")) == 1:
        return True
    return False


def click_not_robot(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "geetest_radar_tip"))
        ).click()
        time.sleep(5)
        driver.find_element(By.CLASS_NAME, "geetest_popup_box")
        return True
    except (NoSuchElementException, TimeoutException):
        return False


def enter_captcha_voice(driver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "geetest_voice"))
    ).click()
    time.sleep(5)


def save_captcha_audio(driver, path):
    audio_src = (
        WebDriverWait(driver, 10)
        .until(EC.presence_of_element_located((By.CLASS_NAME, "geetest_music")))
        .get_attribute("src")
    )
    content = requests.get(audio_src).content
    with open(path + "/audio/captcha_file.wav", "wb") as myaudio:
        myaudio.write(content)
    data, samplerate = soundfile.read(path + "/audio/captcha_file.wav")
    soundfile.write(
        path + "/audio/captcha_file_new.wav", data, samplerate, subtype="PCM_16"
    )


def attempt_captcha(driver, path):
    r = sr.Recognizer()
    with sr.AudioFile(path + "/audio/captcha_file_new.wav") as source:
        audio = r.listen(source)
        try:
            text = r.recognize_vosk(audio, language="de").replace(
                "geben sie ein was sie hören", ""
            )
            for key, value in nums.items():
                text = text.replace(key, value)
            text = text.replace(" ", "")
            text = re.findall("[0-9]+", text)[0]
            print(f"text from audio: {text}")
            driver.find_element(by=By.CLASS_NAME, value="geetest_input").clear()
            driver.find_element(by=By.CLASS_NAME, value="geetest_input").click()
            driver.find_element(by=By.CLASS_NAME, value="geetest_input").send_keys(text)
            time.sleep(5)
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "geetest_submit"))
            ).click()
            time.sleep(5)
            try:
                result_label = driver.find_element(
                    by=By.CLASS_NAME, value="geetest_result_tip"
                ).get_attribute("aria-label")
                print(f"attribute: {result_label}")
                if result_label == "Sorry, keine Übereinstimmung.":
                    print("geetest_result_tip is present, listening failed")
                    return False
                else:
                    return True
            except NoSuchElementException:
                print("geetest_result_tip has not been found, successful listening")
                time.sleep(5)
                return True
        except sr.UnknownValueError:
            print("unknown value error")
            return False


def refresh_captcha(driver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "geetest_refresh"))
    ).click()
    time.sleep(5)


def solve_captcha(driver, path):
    captcha_displayed = click_not_robot(driver)
    if not captcha_displayed:
        return
    enter_captcha_voice(driver)
    while True:
        save_captcha_audio(driver, path)
        if attempt_captcha(driver, path):
            break
        refresh_captcha(driver)


def accept_cookies(driver):
    button = driver.execute_script(
        """return document.querySelector('div#usercentrics-root').shadowRoot.querySelector('button[data-testid="uc-accept-all-button"]')"""
    )
    button.click()
    time.sleep(10)
