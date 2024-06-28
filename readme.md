
## Start

python -m venv .venv

source .venv/bin/activate

pip install -r req.txt

uvicorn main:app --reload

## Test

pytest test_fastapi.py   

## Links

http://127.0.0.1:8000/api/rest/v1/
http://127.0.0.1:8000/api/rest/v1/countries
http://127.0.0.1:8000/api/rest/v1/countries/year/2010