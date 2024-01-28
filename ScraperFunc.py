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

NA = "NA"
r = sr.Recognizer()


class textHelper:
    def __init__(self, text) -> None:
        self._text = text

    @property
    def text(self) -> str:
        return self._text


def driver_startup(url):
    service_path = Service(executable_path="F:/ChromeDriver/chromedriver.exe")
    options = Options()
    # options.add_argument('--headless=new')
    # options.add_argument('--disable-notifications')
    # options.add_argument("--mute-audio")
    driver = webdriver.Chrome(service=service_path, options=options)
    driver.get(url)
    # driver.implicitly_wait(40)
    time.sleep(1000)
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
    path = os.listdir("/ImmoData")

    timestamp = time.time()

    i = 1
    while True:
        print("{} {} {} {}".format("scraping page", i, "from", city))
        all_csvs = list(filter(lambda f: f.endswith(".csv"), path))
        ids_to_read = check_if_id_already_in_export(driver, all_csvs)

        id_list = []
        property_type_list = []
        address_list = []
        region_and_country_list = []
        street_list = []
        apartment_size_list = []
        floor_list = []
        able_to_move_in_list = []
        rooms_list = []
        bathrooms_list = []
        cold_price_list = []
        warm_price_list = []
        labels_list = []
        pets_allowed_list = []
        year_built_list = []
        heating_list = []
        heating_price_list = []
        parking_list = []
        deposit_list = []
        status_list = []
        desc_list = []
        property_url_list = []
        time_list = []

        parent_element = driver.find_element(by=By.ID, value="resultListItems")
        num_listings = len(
            parent_element.find_elements(by=By.XPATH, value="./child::*")
        )

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

            property_type = check_find_elements(
                ".is24qa-typ.grid-item.three-fifths", driver, By.CSS_SELECTOR
            ).text
            address = check_find_elements(
                ".address-block", driver, By.CSS_SELECTOR
            ).text
            region_and_country = check_find_elements(
                ".zip-region-and-country", driver, By.CSS_SELECTOR
            ).text
            street = check_find_elements(
                ".block.font-nowrap.print-hide", driver, By.CSS_SELECTOR
            ).text
            apartment_size = check_find_elements(
                ".is24qa-wohnflaeche-ca.grid-item.three-fifths", driver, By.CSS_SELECTOR
            ).text
            floor = check_find_elements(
                ".is24qa-etage.grid-item.three-fifths", driver, By.CSS_SELECTOR
            ).text
            able_to_move_in = check_find_elements(
                ".is24qa-bezugsfrei-ab.grid-item.three-fifths", driver, By.CSS_SELECTOR
            ).text
            rooms = check_find_elements(
                ".is24qa-zimmer.grid-item.three-fifths", driver, By.CSS_SELECTOR
            ).text
            bathrooms = check_find_elements(
                ".is24qa-badezimmer.grid-item.three-fifths", driver, By.CSS_SELECTOR
            ).text
            cold_price = (
                check_find_elements(
                    ".is24qa-kaltmiete.grid-item.three-fifths", driver, By.CSS_SELECTOR
                )
                .text.replace(".", "")
                .replace(",", ".")
            )
            warm_price = check_find_elements(
                ".is24qa-geschaetzte-warmmiete-main.is24-value.font-semibold",
                driver,
                By.CSS_SELECTOR,
            ).text
            labels = check_labels_element(driver)
            pets_allowed = check_find_elements(
                ".is24qa-haustiere.grid-item.three-fifths", driver, By.CSS_SELECTOR
            ).text
            year_built = check_find_elements(
                ".is24qa-baujahr.grid-item.three-fifths", driver, By.CSS_SELECTOR
            ).text
            heating = check_find_elements(
                ".is24qa-heizungsart.grid-item.three-fifths", driver, By.CSS_SELECTOR
            ).text
            heating_price = check_find_elements(
                ".is24qa-heizkosten.grid-item.three-fifths", driver, By.CSS_SELECTOR
            ).text
            parking = check_find_elements(
                ".is24qa-garage-stellplatz.grid-item.three-fifths",
                driver,
                By.CSS_SELECTOR,
            ).text
            deposit = check_find_elements(
                ".is24qa-kaution-o-genossenschaftsanteile", driver, By.CSS_SELECTOR
            ).text
            status = check_find_elements(
                ".is24qa-objektzustand.grid-item.three-fifths", driver, By.CSS_SELECTOR
            ).text
            desc = check_find_elements(
                ".is24qa-objektbeschreibung.text-content.short-text",
                driver,
                By.CSS_SELECTOR,
            ).text
            property_url = driver.current_url

            id_list.append(_id)
            property_type_list.append(property_type)
            address_list.append(address)
            region_and_country_list.append(region_and_country)
            street_list.append(street)
            apartment_size_list.append(apartment_size)
            floor_list.append(floor)
            able_to_move_in_list.append(able_to_move_in)
            rooms_list.append(rooms)
            bathrooms_list.append(bathrooms)
            cold_price_list.append(cold_price)
            warm_price_list.append(warm_price)
            labels_list.append(labels)
            pets_allowed_list.append(pets_allowed)
            year_built_list.append(year_built)
            heating_list.append(heating)
            heating_price_list.append(heating_price)
            parking_list.append(parking)
            deposit_list.append(deposit)
            status_list.append(status)
            desc_list.append(desc)
            property_url_list.append(property_url)
            time_list.append(timestamp)

            driver.back()
            time.sleep(5)

        temp_df = pd.DataFrame(
            {
                "ID": id_list,
                "Property_type": property_type_list,
                "Street": street_list,
                "Region_and_country": region_and_country_list,
                "Apt_size": apartment_size_list,
                "Floor": floor_list,
                "Move_in": able_to_move_in_list,
                "Nr_of_rooms": rooms_list,
                "Nr_of_bathrooms": bathrooms_list,
                "Cold_price": cold_price_list,
                "Warm_price": warm_price_list,
                "Labels": labels_list,
                "Pets_allowed": pets_allowed_list,
                "Year_built": year_built_list,
                "Heating": heating_list,
                "Heating_price": heating_price_list,
                "Parking": parking_list,
                "Deposit": deposit_list,
                "Status": status_list,
                "Desc": desc_list,
                "URL": property_url_list,
                "Time": time_list,
            }
        )
        csv_export_name = f"{city}_rentals_{i}_page.csv"
        save_data(csv_export_name, temp_df, all_csvs)

        button_check = check_for_last_button(driver)
        if button_check[0]:
            break
        button_check[1].click()
        i += 1
        time.sleep(randrange(5, 10))
