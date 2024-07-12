
## Start

python -m venv .venv

source .venv/bin/activate

pip install -r req.txt

uvicorn main:app --port 8008 --reload

cd `frontend`

uvicorn main:app --reload


Before running the applications create a `.env` file in the backend folder with the following variables and run a Postgres container:

- POSTGRES_HOST=localhost:5432
- POSTGRES_USER="user"
- POSTGRES_PASSWORD="mypassword"
- TABLE_ID="population_data"

docker run --name postgres_db -e POSTGRES_USER=user -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=population_data -p  5432:5432 postgres:latest -d

visit http://localhost:8000/display.html

## OR

1.  First change the data source from Big Query to File, uncomment the file input, and comment the BiqQuery method in`data_util.py` (to use BiqQuery need a Service Account but that is not shared)

2. The app uses the following environment variables which can be put on a `/backend.env` file or create secrets with GCP Secret Manager:

- PROJECT_ID="project id"                                           ##necessary in the case of Biquery only
- DATASET_ID="bigquery dataset id"                                  ##necessary in the case of Biquery only
- GOOGLE_APPLICATION_CREDENTIALS=service account json key           ##necessary in the case of Biquery only and without an authenticated Cloud SDK
- TABLE_ID="table id within BiqQuery dataset and determine the database in Postgres"
- POSTGRES_HOST=localhost:5432
- POSTGRES_USER="user"
- POSTGRES_PASSWORD="mypassword"

3. Create an image for the API: 
docker build -f back.Dockerfile -t fastapi_backend_app .

4. Create an image for the Frontend: 
docker build -f front.Dockerfile -t fastapi_frontend_app .

5. Compose up: 
(sudo) docker-compose --env-file ./backend/.env up

visit http://localhost:8000/display.html

## Test

pytest test_fastapi.py   

## Links

- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/api/rest/v1/countries/save?page=1size=40
- http://127.0.0.1:8000/api/rest/v1/countries?page=1size=40
- http://127.0.0.1:8000/api/rest/v1/countries/year/2010?page=1size=40
- http://127.0.0.1:8000/api/rest/v1/countries/code/HUN?page=1size=40

