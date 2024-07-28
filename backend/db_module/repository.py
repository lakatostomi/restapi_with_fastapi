from sqlalchemy.orm import Session
from . import models 
from . import schemas
import logging
from fastapi import HTTPException

logger = logging.getLogger('uvicorn.error')

def get_all_countries(db: Session):
    logger.info("Querying all countries!")
    return db.query(models.Country).all()

def get_countries_by_code(db: Session, code: str):
    logger.info(f"Querying countries with code={code}")
    return db.query(models.Country).filter(models.Country.country_code == code).all()

def get_countries_by_year(db: Session, year: int):
    logger.info(f"Querying countries with year={year}")
    return db.query(models.Country).filter_by(year=year).all()

def save_country(db: Session, country: schemas.CountryCreate):
    logger.info(f"Saving new country={country}")
    db_country = create_country(country)
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return db_country

def save_all_countries(db: Session, country_list: list[schemas.CountryCreate]):
    country = db.query(models.Country).first()
    if country == None:
        logger.info("Saving country list to DB!")
        db_country_list = []
        for country in country_list:
            db_country = create_country(country)
            db_country_list.append(db_country)
    
        db.add_all(db_country_list)
        db.commit()
        logger.info(f"Saving finished, number of inserted entities={len(db_country_list)}")
        

def create_country(country: schemas.CountryCreate):
    return models.Country(**country.model_dump())

def delete_country(db: Session, id: int):
    country = db.get(models.Country, id)
    if not country:
        raise HTTPException(status_code=404, detail=f"No country exist with id={id}!")
    db.delete(country)
    db.commit()

def update_country(db: Session, country: schemas.CountryCreate, id: int):
    country_in_db = db.get(models.Country, id)
    if not country_in_db:
        raise HTTPException(status_code=404, detail=f"No country exist with id={id}!")
    stored_country_model = schemas.Country(id=country_in_db.id,country_name=country_in_db.country_name, country_code=country_in_db.country_code, year=country_in_db.year, population=country_in_db.population)
    update_data = country.model_dump(exclude_unset=True)
    update_country = stored_country_model.model_copy(update=update_data)
    db_county = create_country(update_country)
    db.merge(db_county)
    db.commit()
    db.refresh
    return db_county

