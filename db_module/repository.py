from sqlalchemy.orm import Session
from . import models 
from . import schemas

def get_all_countries(db: Session):
    return db.query(models.Country).all()

def get_countries_by_code(db: Session, code: str):
    return db.query(models.Country).filter(models.Country.country_code == code).all()

def get_countries_by_year(db: Session, year: int):
    return db.query(models.Country).filter_by(year=year).all()

def save_country(db: Session, country: schemas.CountryCreate):
    db_country = create_country(country)
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    db.close()
    return db_country

def save_all_countries(db: Session, country_list: list[schemas.CountryCreate]):
    db_country_list = []
    for country in country_list:
        db_country = create_country(country)
        db_country_list.append(db_country)
    
    db.add_all(db_country_list)
    print(len(country_list))
    db.commit()

def create_country(country: schemas.CountryCreate):
    return models.Country(**country.model_dump())

def delete_country(db: Session, id: int):
    pass #later will be declared

def update_country(db: Session, country: schemas.CountryCreate):
    pass #later will be declared