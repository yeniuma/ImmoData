import ScraperFunc as SF


page = "https://www.immobilienscout24.de/Suche/at/wien/wien/wohnung-mieten?pricetype=rentpermonth&enteredFrom=result_list"
city = "Vienna"

driver = SF.driver_startup(page)


SF.scrape_immoscout_rentals(driver,"Vienna")
