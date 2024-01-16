import ScraperFunc as SF
import CaptchaFunc as CF

page = "https://www.immobilienscout24.de/Suche/at/wien/wien/wohnung-mieten?pricetype=rentpermonth&enteredFrom=result_list"
city = "Vienna"

driver = SF.driver_startup(page)
CF.click_not_robot(driver)


SF.scrape_immoscout_rentals("Vienna")
