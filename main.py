from fastapi import FastAPI, Path, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from typing import Annotated
import exception
import countryservice as service
import Country as model
import logging

app = FastAPI(root_path="/api/rest/v1")
#app.mount("/", StaticFiles(directory="static", html=True), name="static")

logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('uvicorn.error')

@app.exception_handler(exception.ResourceNotExist)
async def handle_exception(request: Request, ex: exception.ResourceNotExist):
    return JSONResponse(status_code=404,
                        content={"message": f"{ex.message}", "time": f"{ex.when}", "statusCode": "404", "status": "Not found"})

@app.get("/countries", response_model=list[model.Country])
async def findAll():
   logger.info("Returning result list")
   return service.country_list

@app.get("/countries/code/{code}", response_model=list[model.Country])
async def findByCode(code: Annotated[str, Path(min_length=3, max_length=4)]):
    result_list = service.findByCode(code)
    return result_list

@app.get("/countries/year/{year}", response_model=list[model.Country])
async def findByCode(year: Annotated[int, Path(min=1960, max=2010)]): 
    result_list = service.findByYear(year)
    return result_list