from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from random import randrange
import time
import pandas as pd
import os
import speech_recognition as sr
import CaptchaFunc as CF

NA = "NA"
r = sr.Recognizer()


class textHelper:
    def __init__(self, text) -> None:
        self._text = text

    @property
    def text(self) -> str:
        return self._text


def get_parameters_from_user():
    parameters_dict = {
        "city": "",
        "min_price": "",
        "max_price": "",
        "min_sqm": "",
        "max_sqm": "",
        "min_rooms": "",
        "max_rooms": "",
    }
    print("Please input the German name of the city you want to scrape listings for:")
    parameters_dict["city"] = str(input())

    print("Please input the minimum price or press Enter to skip:")
    parameters_dict["min_price"] = float(input())

    print("Please input the maximum price or press Enter to skip:")
    parameters_dict["max_price"] = float(input())

    print("Please input the minimum sqm or press Enter to skip:")
    parameters_dict["min_sqm"] = float(input())

    print("Please input the maximum sqm or press Enter to skip:")
    parameters_dict["max_sqm"] = float(input())

    print("Please input the minimum number of rooms or press Enter to skip:")
    parameters_dict["min_rooms"] = int(input())

    print("Please input the maximum number of rooms or press Enter to skip:")
    parameters_dict["max_rooms"] = int(input())

    return parameters_dict


def check_libraries():
    exports = "./exports"
    audio = "./audio"
    if not os.path.exists(exports):
        print("nincs export")
        os.mkdir(exports)
    if not os.path.exists(audio):
        print("nincs audio")
        os.mkdir(audio)


def url_builder(
    city, min_price="", max_price="", min_sqm="", max_sqm="", min_rooms="", max_rooms=""
):
    filter_dict = {
        "price": f"price={min_price}-{max_price}",
        "sqm": f"livingspace={min_sqm}-{max_sqm}",
        "num_rooms": f"numberofrooms={min_rooms}-{max_rooms}",
    }
    city = city.lower()
    result = "&".join(filter_dict.values()) + "&"
    url = f"https://www.immobilienscout24.de/Suche/at/{city}/{city}/wohnung-mieten?{result}pricetype=rentpermonth&enteredFrom=result_list"
    return url


def driver_startup(url):
    service_path = Service(executable_path="F:/ChromeDriver/chromedriver.exe")
    options = Options()
    #options.add_argument('--headless=new')
    options.add_argument('--disable-notifications')
    options.add_argument("--mute-audio")
    driver = webdriver.Chrome(service=service_path, options=options)
    driver.get(url)
    time.sleep(10)
    return driver


def save_data(csv_export_name, df, exported_csvs):
    print(csv_export_name)
    print(exported_csvs)
    if df.empty:
        return

    if csv_export_name in exported_csvs:
        df.to_csv(csv_export_name, mode="a", encoding="utf-8-sig", header=False)
    else:
        df.to_csv(csv_export_name, encoding="utf-8-sig")


def check_for_last_button(driver):
    try:
        driver.find_element(
            by=By.CSS_SELECTOR,
            value=".p-items.p-next.vertical-center-container.disabled",
        )
        return [True, None]
    except NoSuchElementException:
        temp = driver.find_element(
            by=By.CSS_SELECTOR, value=".p-items.p-next.vertical-center-container"
        )
        return [False, temp]


def check_if_id_already_in_export(driver, exported_csvs):
    if len(exported_csvs) == 0:
        exported_ids = list()
    else:
        df = pd.concat((pd.read_csv(f) for f in exported_csvs), ignore_index=True)
        exported_ids = df["ID"].tolist()
    online_listing_ids = []
    parent_element = driver.find_element(by=By.ID, value="resultListItems")
    num_listings = len(parent_element.find_elements(by=By.XPATH, value="./child::*"))
    for j in range(num_listings):
        parent_element = driver.find_element(by=By.ID, value="resultListItems")
        listing = parent_element.find_elements(by=By.XPATH, value="./child::*")[j]
        if listing.get_attribute("class") != "result-list__listing ":
            continue
        else:
            online_listing_ids.append(listing.get_attribute("data-id"))
    ids_to_read = list(set(online_listing_ids) - set(exported_ids))
    return ids_to_read


def check_find_elements(selector_value, driver, by):
    if (
        len(driver.find_elements(by=by, value=selector_value)) == 0
        or driver.find_elements(by=by, value=selector_value)[0].text == ""
        or driver.find_elements(by=by, value=selector_value)[0].text.isspace()
    ):
        temp = textHelper(NA)
    else:
        temp = driver.find_elements(by=by, value=selector_value)[0]
    return temp


def check_labels_element(driver):
    try:
        labels_parent_element = driver.find_element(
            by=By.CSS_SELECTOR, value=".criteriagroup.boolean-listing.padding-top-l"
        )
    except NoSuchElementException:
        return NA

    labels_child_elements = labels_parent_element.find_elements(
        by=By.XPATH, value="./child::*"
    )
    return ",".join([k.text for k in labels_child_elements if k.text != ""])


def scrape_immoscout_rentals(driver, city):
    files = os.listdir("/ImmoData")
    path = "/ImmoData/exports"
    timestamp = time.time()

    CF.solve_captcha(driver, path)
    CF.accept_cookies(driver)

    i = 1
    while True:
        CF.solve_captcha(driver, path)
        print(f"scraping page {i} from {city}")
        all_csvs = [f for f in files if f.endswith(".csv")]
        ids_to_read = check_if_id_already_in_export(driver, all_csvs)

        data = {
            "ID": [],
            "Property_type": [],
            "Street": [],
            "Region_and_country": [],
            "Address": [],
            "Apt_size": [],
            "Floor": [],
            "Move_in": [],
            "Nr_of_rooms": [],
            "Nr_of_bathrooms": [],
            "Cold_price": [],
            "Warm_price": [],
            "Labels": [],
            "Pets_allowed": [],
            "Year_built": [],
            "Heating": [],
            "Heating_price": [],
            "Parking": [],
            "Deposit": [],
            "Status": [],
            "Desc": [],
            "URL": [],
            "Time": [],
        }

        parent_element = driver.find_element(by=By.ID, value="resultListItems")
        num_listings = len(
            parent_element.find_elements(by=By.XPATH, value="./child::*")
        )
        print(f"for előtt:{i}")
        for j in range(num_listings):
            parent_element = WebDriverWait(driver, 30000).until(
                EC.presence_of_element_located((By.ID, "resultListItems"))
            )
            listing = parent_element.find_elements(by=By.XPATH, value="./child::*")[j]

            if listing.get_attribute("class") != "result-list__listing ":
                continue

            _id = listing.get_attribute("data-id")
            if _id not in ids_to_read:
                continue

            listing.find_element(
                by=By.CSS_SELECTOR,
                value=".result-list-entry__brand-title.font-h6.onlyLarge.font-ellipsis.font-regular.nine-tenths",
            ).click()
            time.sleep(3)
            print(f"attribútomok előtt:{i}")
            attributes = [
                (".is24qa-typ.grid-item.three-fifths", "Property_type"),
                (".address-block", "Address"),
                (".zip-region-and-country", "Region_and_country"),
                (".block.font-nowrap.print-hide", "Street"),
                (".is24qa-wohnflaeche-ca.grid-item.three-fifths", "Apt_size"),
                (".is24qa-etage.grid-item.three-fifths", "Floor"),
                (".is24qa-bezugsfrei-ab.grid-item.three-fifths", "Move_in"),
                (".is24qa-zimmer.grid-item.three-fifths", "Nr_of_rooms"),
                (".is24qa-badezimmer.grid-item.three-fifths", "Nr_of_bathrooms"),
                (".is24qa-kaltmiete.grid-item.three-fifths", "Cold_price"),
                (
                    ".is24qa-geschaetzte-warmmiete-main.is24-value.font-semibold",
                    "Warm_price",
                ),
                (".is24qa-haustiere.grid-item.three-fifths", "Pets_allowed"),
                (".is24qa-baujahr.grid-item.three-fifths", "Year_built"),
                (".is24qa-heizungsart.grid-item.three-fifths", "Heating"),
                (".is24qa-heizkosten.grid-item.three-fifths", "Heating_price"),
                (".is24qa-garage-stellplatz.grid-item.three-fifths", "Parking"),
                (".is24qa-kaution-o-genossenschaftsanteile", "Deposit"),
                (".is24qa-objektzustand.grid-item.three-fifths", "Status"),
                (".is24qa-objektbeschreibung.text-content.short-text", "Desc"),
            ]

            for attr in attributes:
                if attr[1] == "Cold_price":
                    data[attr[1]].append(
                        check_find_elements(
                            attr[0], driver, By.CSS_SELECTOR
                        ).text.replace(".", "")
                    )
                else:
                    data[attr[1]].append(
                        check_find_elements(attr[0], driver, By.CSS_SELECTOR).text
                    )

            data["Labels"].append(check_labels_element(driver))
            data["ID"].append(_id)
            data["URL"].append(driver.current_url)
            print(f"time append előtt:{i}")
            data["Time"].append(timestamp)
            print(f"time append után:{i}")
            driver.back()
            time.sleep(5)
        print(f"for után:{i}")
        temp_df = pd.DataFrame(data)
        csv_export_name = f"{city}_rentals_{i}_page.csv"
        save_data(csv_export_name, temp_df, all_csvs)
        print(f"mentés után:{i}")
        button_check = check_for_last_button(driver)
        if button_check[0]:
            break
        button_check[1].click()
        print(f"+= előtt:{i}")
        i += 1
        time.sleep(randrange(5, 10))