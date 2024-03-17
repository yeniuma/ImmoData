import ScraperFunc as SF
#import time
import DataCleanFunc as DCF
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

export_path = "F:/ImmoData/exports"

raw_data = DCF.get_concatonated_exports(export_path)

transormed_data = DCF.transform_raw_data(raw_data)

transormed_data.to_csv("F:/ImmoData/transformed/test.csv", encoding="utf-8-sig", index=False)