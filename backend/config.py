from dotenv import load_dotenv
import os
from os.path import join, dirname

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

PROJECT_ID = os.environ.get("PROJECT_ID")
DATASET_ID = os.environ.get("DATASET_ID")
TABLE_ID = os.environ.get("TABLE_ID")

dataset_str = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PWD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")

