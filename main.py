import ScraperFunc as SF
import time
#TODO: take apart SF.scrape_immoscout_rentals function somehow so it fits this flow:
# captcha
# cookie
# while true
#   captcha
#   get relevant ids
#      for
#       get data
#       save data
#   if there are more pages
#       get next page


parameters = SF.get_parameters_from_user()

SF.check_libraries()

page = SF.url_builder(
    parameters["city"],
    parameters["min_price"],
    parameters["max_price"],
    parameters["min_sqm"],
    parameters["max_sqm"],
    parameters["min_rooms"],
    parameters["max_rooms"],
)


driver = SF.driver_startup(page)

SF.scrape_immoscout_rentals(driver, parameters["city"])
