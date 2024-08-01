
import json
import logging
from db_module import repository as repository 
from db_module import schemas as schemas
from sqlalchemy.orm import Session
from biqquery_module import repository as biqquery

logger = logging.getLogger('uvicorn.error')

country_list = []

def init_data():
    #logger.info("Querying from Big Query is skipped, do not forget to uncomment before production!!!!")
    if len(country_list) == 0:
      query_result = biqquery.get_all_countries()
      for row in query_result:
        country = schemas.CountryCreate(country_name= row["country_name"], country_code=row["country_code"], year=row["year"], population=str(row["population"]))
        country_list.append(country)
       
# Initializing data from file

# def init_data():
#   with open("../population_data_jsonline.json", "r") as user_file:
#     logger.info("Initialzing data from file...")
#     country_list = []
#     for x in user_file:
#         parsed = json.loads(x)
#         country = schemas.CountryCreate(country_name=parsed['country_name'], country_code=parsed['country_code'], year=parsed['year'], population=f"{parsed['population']}")
#         country_list.append(country)
#     logger.info(f"...file reading finished")
    
