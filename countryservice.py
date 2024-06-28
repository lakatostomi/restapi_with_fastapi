import Country as model
import json
import logging
import exception

country_list = []

logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('uvicorn.error')

file_loc = "./population_data_jsonline.json"
# file_loc = "/home/tamas/Documents/population_data_jsonline.json"

with open(file_loc, "r") as user_file:
    logger.info("Reading file...")
    for x in user_file:
        parsed = json.loads(x)
        country = model.Country(country_name=parsed['countryName'], country_code=parsed['countryCode'], year=parsed['year'], population=f"{parsed['value']}")
        country_list.append(country)
    logger.info(f"...finished successfully, list size={len(country_list)}")    

def findByCode(code: str):
    logger.info(f"Serching for countries with \'{code}\' code")
    result_list = [country for country in country_list if code == country.country_code]
    if result_list:
      return result_list
    raise exception.ResourceNotExist(message=f"No data exists with code={code}")    

def findByYear(year: int):
    logger.info(f"Serching for countries with year=\'{year}\'")
    result_list = [country for country in country_list if year == country.year]
    if result_list:
      return result_list
    raise exception.ResourceNotExist(message=f"No data exists with year={year}")