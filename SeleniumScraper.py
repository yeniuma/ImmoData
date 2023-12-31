from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from random import randrange
import time
import pandas as pd


page = "https://www.immobilienscout24.de/Suche/at/wien/wien/wohnung-mieten?pricetype=rentpermonth&enteredFrom=result_list"
city = "Vienna"
NA = "NA"

#implementalando: figyelje az id-t, hogy ne exportaljon duplicate listinget, scraping elejen be kell olvasnia a mar meglevo id-kat

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
    options.add_argument("--mute-audio")
    driver = webdriver.Chrome(service=service_path, options=options)
    driver.get(url)
    # driver.implicitly_wait(40)
    ##accept_cookies = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="uc-center-container"]/div[2]/div/div/div/button[2]')))
    # driver.execute_script("arguments[0].click()", accept_cookies)
    # driver.find_element(by=By.XPATH, value='/html/body/div[6]//div/div/div[2]/div/div[2]/div/div[2]/div/div/div/button[2]').click()
    time.sleep(20)
    return driver


def check_find_elements(selector_value, driver):
    if (
        len(driver.find_elements(by=By.CSS_SELECTOR, value=selector_value)) == 0
        or driver.find_elements(by=By.CSS_SELECTOR, value=selector_value)[0].text == ""
        or driver.find_elements(by=By.CSS_SELECTOR, value=selector_value)[
            0
        ].text.isspace()
    ):
        temp = textHelper(NA)
    else:
        temp = driver.find_elements(by=By.CSS_SELECTOR, value=selector_value)[0]
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
    return ",".join([k.text for k in labels_child_elements if k.text != ''])


def scrape_immoscout_rentals(city):
    driver = driver_startup(page)

    i = 1
    while True:
        print("{} {} {} {}".format("scraping page", i, "from", city))

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
        cold_price_per_sqm_list = []
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

        parent_element = driver.find_element(by=By.ID, value="resultListItems")
        num_listings = len(
            parent_element.find_elements(by=By.XPATH, value="./child::*")
        )

        for j in range(num_listings):
            parent_element = driver.find_element(by=By.ID, value="resultListItems")
            listing = parent_element.find_elements(by=By.XPATH, value="./child::*")[j]
            if listing.get_attribute("class") != "result-list__listing ":
                continue
            else:
                _id = listing.get_attribute("data-id")
                listing.find_element(
                    by=By.CSS_SELECTOR,
                    value=".result-list-entry__brand-title.font-h6.onlyLarge.font-ellipsis.font-regular.nine-tenths",
                ).click()
                time.sleep(3)
            property_type = check_find_elements(
                ".is24qa-typ.grid-item.three-fifths", driver
            ).text
            address = check_find_elements(".address-block", driver).text
            region_and_country = check_find_elements(
                ".zip-region-and-country", driver
            ).text
            street = check_find_elements(".block.font-nowrap.print-hide", driver).text
            apartment_size = check_find_elements(
                ".is24qa-wohnflaeche-ca.grid-item.three-fifths", driver
            ).text
            floor = check_find_elements(
                ".is24qa-etage.grid-item.three-fifths", driver
            ).text
            able_to_move_in = check_find_elements(
                ".is24qa-bezugsfrei-ab.grid-item.three-fifths", driver
            ).text
            rooms = check_find_elements(
                ".is24qa-zimmer.grid-item.three-fifths", driver
            ).text
            bathrooms = check_find_elements(
                ".is24qa-badezimmer.grid-item.three-fifths", driver
            ).text
            cold_price = check_find_elements(".is24qa-kaltmiete.grid-item.three-fifths", driver).text.replace('.','').replace(',','.')
            cold_price_per_sqm = driver.find_elements(by=By.XPATH,value='/html/body/div[2]/div[4]/div[1]/div/div[3]/div[2]/div[1]/div[2]/div[1]/div/div[2]/span')[0].text
            warm_price = check_find_elements(
                ".is24qa-geschaetzte-warmmiete-main.is24-value.font-semibold", driver
            ).text
            labels = check_labels_element(driver)
            pets_allowed = check_find_elements(
                ".is24qa-haustiere.grid-item.three-fifths", driver
            ).text
            year_built = check_find_elements(
                ".is24qa-baujahr.grid-item.three-fifths", driver
            ).text
            heating = check_find_elements(
                ".is24qa-heizungsart.grid-item.three-fifths", driver
            ).text
            heating_price = check_find_elements(
                ".is24qa-heizkosten.grid-item.three-fifths", driver
            ).text
            parking = check_find_elements(
                ".is24qa-garage-stellplatz.grid-item.three-fifths", driver
            ).text
            deposit = check_find_elements(
                ".is24qa-kaution-o-genossenschaftsanteile", driver
            ).text
            status = check_find_elements(
                ".is24qa-objektzustand.grid-item.three-fifths", driver
            ).text
            desc = check_find_elements(
                ".is24qa-objektbeschreibung.text-content.short-text", driver
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
            cold_price_per_sqm_list.append(cold_price_per_sqm)
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
                "Cold_price_per_sqm": cold_price_per_sqm_list,
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
            }
        )
        temp_df.to_csv(f"{city}rentals_{i}_page.csv", encoding="utf-8-sig")

        last_button_found = False
        try:
            driver.find_element(
                by=By.CSS_SELECTOR,
                value=".p-items.p-next.vertical-center-container.disabled",
            )
            last_button_found = True
        except NoSuchElementException:
            driver.find_element(
                by=By.CSS_SELECTOR, value=".p-items.p-next.vertical-center-container"
            ).click()

        if last_button_found:
            break

        # ideiglenes
        i += 1

        if i > 1:
            break
        time.sleep(randrange(5, 10))


scrape_immoscout_rentals("Vienna")
