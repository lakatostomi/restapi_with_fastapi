from fastapi import FastAPI, Path, Request, status, Body, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
import data_util as util
import logging
import db_module.models as models ,db_module.schemas as schemas
from db_module.database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi_pagination import add_pagination, paginate
from fastapi_pagination.links import Page
import exception
from db_module import repository
from firebase_admin import auth
import auth_router

models.Base.metadata.create_all(bind=engine)

async def init_data(app: FastAPI):
   util.init_data()
   yield

app = FastAPI(root_path="/api/rest/v1", lifespan=init_data)
app.include_router(auth_router.router)
add_pagination(app)

origins = [
    "*"
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
                        content={"message": f"{ex.message}", "time": f"{ex.when}", "statusCode": status.HTTP_404_NOT_FOUND, "status": "Not Found"})


@app.get("/countries/save", response_model=Page[schemas.Country])
def save_db(db: Session = Depends(get_db), query: Session = Depends(get_db)):
   repository.save_all_countries(db=db, country_list=util.country_list)
   return paginate(repository.get_all_countries(db=query))

@app.get("/countries", response_model=Page[schemas.Country])
def get_all_countries(db: Session = Depends(get_db)):
   return paginate(repository.get_all_countries(db=db))

@app.get("/countries/code/{code}", response_model=Page[schemas.CountryBase])
def find_by_code(code: Annotated[str, Path()], db: Session = Depends(get_db)):
    result_list = paginate(repository.get_countries_by_code(db=db, code=code))
    if result_list.items:
      return result_list
    raise exception.ResourceNotExist(message=f"No data exists with code=\'{code}\'")

@app.get("/countries/year/{year}", response_model=Page[schemas.Country])
def find_by_year(year: Annotated[int, Path()], db: Session = Depends(get_db)): 
    result_list = paginate(repository.get_countries_by_year(db=db, year=year))
    if result_list.items:
      return result_list
    raise exception.ResourceNotExist(message=f"No data exists with year=\'{year}\'")


def verify_token(cred: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))):
   try:
      print(cred.credentials)
      decodod_token = auth.verify_id_token(cred.credentials)
   except Exception as ex:
      raise HTTPException(status_code=401, detail=f"Authentication error: {ex}", headers={"WWW-Authenticate": "Bearer"}) 

@app.post("/countries", response_model=schemas.Country, status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_token)])
def save_country(country: Annotated[schemas.CountryCreate, Body()], db: Session = Depends(get_db)):
   return repository.save_country(db=db, country=country)

@app.patch("/countries/update/{id}", response_model=schemas.Country, dependencies=[Depends(verify_token)])
def update_country(id: Annotated[int, Path()], update_country: Annotated[schemas.CountryCreate, Body()], db: Session = Depends(get_db)):
   return repository.update_country(db=db, country=update_country, id=id)

@app.delete("/countries/delete/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_token)])
def delete_country(id: Annotated[int, Path()], db: Session = Depends(get_db)):
   return repository.delete_country(db=db, id=id)
