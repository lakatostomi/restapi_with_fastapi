
import json
import logging
from db_module import repository as repository 
from db_module import schemas as schemas
from sqlalchemy.orm import Session

logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('uvicorn.error')

def init_data(db: Session):
  with open("./population_data_jsonline.json", "r") as user_file:
    logger.info("Initialzing data from file...")
    country_list = []
    for x in user_file:
        parsed = json.loads(x)
        country = schemas.CountryCreate(country_name=parsed['countryName'], country_code=parsed['countryCode'], year=parsed['year'], population=f"{parsed['value']}")
        country_list.append(country)
    logger.info(f"...file reading finished, saving data to DB")    
    repository.save_all_countries(db=db, country_list=country_list)
    logger.info("data saved, app is ready!")  
    return len(country_list)
