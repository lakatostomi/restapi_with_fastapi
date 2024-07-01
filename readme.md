
## Start

python -m venv .venv

source .venv/bin/activate

pip install -r req.txt

uvicorn main:app --port 8008 --reload

cd `frontend`

uvicorn main:app --reload

visit http://localhost:8000/display.html

Before running the appication configure the database server at `db_module/database.py` file. App was tested on a local Postgre containter, to initialize data send request to http://127.0.0.1:8000/api/rest/v1/countries/save endpoint that will read the data from file and save them to the DB. 

## Test

pytest test_fastapi.py   

## Links

http://127.0.0.1:8000/api/rest/v1/docs
http://127.0.0.1:8000/api/rest/v1/countries
http://127.0.0.1:8000/api/rest/v1/countries/year/2010
http://127.0.0.1:8000/api/rest/v1/countries/code/HUN

