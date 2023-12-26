from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

page = 'https://www.immobilienscout24.de/Suche/at/wien/wien/wohnung-mieten?pricetype=rentpermonth&enteredFrom=result_list'
city = 'Vienna'

class textHelper :
    def __init__(self, text) -> None:
        self._text = text
    
    @property
    def text(self) -> str:
        return self._text

def driver_startup(url):
    service_path = Service(executable_path='F:/ChromeDriver/chromedriver.exe')
    options = Options()
    #options.add_argument('--headless=new')
    driver = webdriver.Chrome(service=service_path, options=options)
    driver.get(url)
    time.sleep(20)
    return driver

def check_find_elements(selector_value, driver):
    temp_list = []
    if len(driver.find_elements(by=By.CSS_SELECTOR,value=selector_value)) == 0:
        temp_list = [textHelper('NA')]
    else:
        temp_list = driver.find_elements(by=By.CSS_SELECTOR,value=selector_value)[:1]
    return temp_list

def scrape_immoscout_rentals(city):
    rentals_df = pd.DataFrame()

    property_type = []
    address = []
    region_and_country = []
    street = []
    apartment_size = []
    floor = []
    able_to_move_in = []
    rooms = []
    bathrooms = []
    cold_price = []
    cold_price_per_sqm = []
    warm_price = []
    labels = []
    pets_allowed = []
    year_built = []
    heating = []
    heating_price = []
    parking = []
    deposit = []
    status = []
    desc = []
    property_url = []
    website = []

    driver = driver_startup(page)

    for j in range(5):
        driver.find_element(by=By.ID, value = f'listing-{j}-slide-0').click()
        time.sleep(10)
        driver.back()
        time.sleep(10)
    #driver.find_element(by=By.ID,value='listing-0-slide-0').click()

    i = 1
    while True :
        time.sleep(2)
        print("{} {} {} {}".format('scraping page', i,'from', city))
        property_type_list = check_find_elements('.is24qa-typ.grid-item.three-fifths', driver)
        address_list = check_find_elements('.address-block', driver)
        region_and_country_list = check_find_elements('.zip-region-and-country', driver)
        street_list = check_find_elements('.block.font-nowrap.print-hide', driver)
        apartment_size_list = check_find_elements('.is24qa-wohnflaeche-ca.grid-item.three-fifths', driver)
        floor_list = check_find_elements('.is24qa-etage.grid-item.three-fifths', driver)
        able_to_move_in_list = check_find_elements('.is24qa-bezugsfrei-ab.grid-item.three-fifths', driver)
        rooms_list = check_find_elements('.is24qa-zimmer.grid-item.three-fifths', driver)
        bathrooms_list = check_find_elements('.is24qa-badezimmer.grid-item.three-fifths', driver)
        cold_price_list = check_find_elements('.is24-preis-value', driver)
        cold_price_per_sqm_list = check_find_elements('.is24qa-kaltmiete-main-label.is24-label.font-s', driver)
        warm_price_list = check_find_elements('.is24qa-geschaetzte-warmmiete-main.is24-value.font-semibold', driver)
        labels_list = check_find_elements('.criteriagroup.boolean-listing.padding-top-l', driver)
        pets_allowed_list = check_find_elements('.is24qa-haustiere.grid-item.three-fifths', driver)
        year_built_list = check_find_elements('.is24qa-baujahr.grid-item.three-fifths', driver)
        heating_list = check_find_elements('.is24qa-heizungsart.grid-item.three-fifths', driver)
        heating_price_list = check_find_elements('.is24qa-heizkosten.grid-item.three-fifths', driver)
        parking_list = check_find_elements('.is24qa-garage-stellplatz.grid-item.three-fifths', driver)
        deposit_list = check_find_elements('.is24qa-kaution-o-genossenschaftsanteile', driver)
        status_list = check_find_elements('.is24qa-objektzustand.grid-item.three-fifths', driver)
        desc_list = check_find_elements('.is24qa-lage.text-content.short-text', driver)
        property_url_list = driver.current_url
        website_list = website
        for property_type_item, address_item, region_and_country_item, street_item, apartment_size_item, floor_item, able_to_move_in_item, rooms_item, bathrooms_item, cold_price_item, cold_price_per_sqm_item, warm_price_item, labels_item, pets_allowed_item, year_built_item, heating_item, heating_price_item, parking_item, deposit_item, status_item, desc_item in zip(property_type_list, region_and_country_list, address_list, street_list,apartment_size_list,floor_list,able_to_move_in_list,rooms_list,bathrooms_list,cold_price_list,cold_price_per_sqm_list,warm_price_list,labels_list,pets_allowed_list,year_built_list,heating_list,heating_price_list,parking_list,deposit_list,status_list,desc_list):
            property_type.append(property_type_item.text)
            address.append(address_item.text)
            region_and_country.append(region_and_country_item.text)
            street.append(street_item.text)
            apartment_size.append(apartment_size_item.text)
            floor.append(floor_item.text)
            able_to_move_in.append(able_to_move_in_item.text)
            rooms.append(rooms_item.text)
            bathrooms.append(bathrooms_item.text)
            cold_price.append(cold_price_item.text)
            cold_price_per_sqm.append(cold_price_per_sqm_item.text)
            warm_price.append(warm_price_item.text)
            labels.append(labels_item.text)
            pets_allowed.append(pets_allowed_item.text)
            year_built.append(year_built_item.text)
            heating.append(heating_item.text)
            heating_price.append(heating_price_item.text)
            parking.append(parking_item.text)
            deposit.append(deposit_item.text)
            status.append(status_item.text)
            desc.append(desc_item.text)
            property_url.append(property_url_list)
            website.append(website_list)
        break

    temp_df = pd.DataFrame({'Property_type': property_type, 'Street':street, 'Region_and_country': region_and_country, 'Apt_size': apartment_size, 'Floor':floor,
                            'Move_in':able_to_move_in, 'Nr_of_rooms': rooms, 'Nr_of_bathrooms':bathrooms, 'Cold_price':cold_price, 'Cold_price_per_sqm': cold_price_per_sqm,
                            'Warm_price':warm_price, 'Labels': labels, 'Pets_allowed' : pets_allowed, 'Year_built': year_built, 'Heating': heating, 'Heating_price': heating_price, 'Parking': parking,
                            'Deposit': deposit, 'Status': status, 'Desc': desc, 'URL': property_url})
    print('Total numbers of properties available in ' + city + ' is ' + str(temp_df.shape[0]))

    rentals_df = pd.concat([rentals_df, temp_df], ignore_index=True)

    return rentals_df

test_df = scrape_immoscout_rentals('Vienna')

with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(test_df)
