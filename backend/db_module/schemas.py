from pydantic import BaseModel

class CountryBase(BaseModel):
    country_name: str 
    country_code: str
    year: int
    population: str

class CountryCreate(CountryBase):
    pass

class Country(CountryBase):
    id: int

    class Config:
        from_attributes = True