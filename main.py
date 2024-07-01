from fastapi import FastAPI, Path, Request, status, Body
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
import exception
import data_util as service
import logging
from fastapi import Depends
from sqlalchemy.orm import Session
import db_module.repository as repository, db_module.models as models ,db_module.schemas as schemas
from db_module.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(root_path="/api/rest/v1")

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('uvicorn.error')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.exception_handler(exception.ResourceNotExist)
async def handle_exception(request: Request, ex: exception.ResourceNotExist):
    return JSONResponse(status_code=404,
                        content={"message": f"{ex.message}", "time": f"{ex.when}", "statusCode": status.HTTP_404_NOT_FOUND, "status": "Not found"})

@app.get("/save", status_code=status.HTTP_201_CREATED)
def inti_data(db: Session = Depends(get_db)):
   rows_inserted = service.init_data(db=db)
   return f"Data is initialized! Number of inserted rows={rows_inserted}"

@app.get("/countries", response_model=list[schemas.Country])
def get_all_countries(db: Session = Depends(get_db)):
   logger.info("Returning result list")
   return repository.get_all_countries(db=db)

@app.get("/countries/code/{code}", response_model=list[schemas.Country])
def findByCode(code: Annotated[str, Path(min_length=3, max_length=4)], db: Session = Depends(get_db)):
    result_list = repository.get_countries_by_code(db=db, code=code)
    if result_list:
      return result_list
    raise exception.ResourceNotExist(message=f"No data exists with code=\'{code}\'")

@app.get("/countries/year/{year}", response_model=list[schemas.Country])
def findByCode(year: Annotated[int, Path(min=1960, max=2010)], db: Session = Depends(get_db)): 
    result_list = repository.get_countries_by_year(db=db, year=year)
    if result_list:
      return result_list
    raise exception.ResourceNotExist(message=f"No data exists with year=\'{year}\'")

@app.post("/countries", response_model=schemas.Country)
def save_country(country: Annotated[schemas.CountryCreate, Body()], db: Session = Depends(get_db)):
   return repository.save_country(db=db, country=country)