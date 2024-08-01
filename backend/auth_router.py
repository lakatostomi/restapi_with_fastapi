from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from config import settings
import random
import logging
from firebase_admin import auth, credentials, firestore
import pyrebase
import firebase_admin
import json

router = APIRouter()

logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('uvicorn.error')

cred = credentials.Certificate(settings.FIREBASE_AUTH_SA_KEY)
#cred = credentials.Certificate("./fastapi_app_sa_key.json")
firebase = firebase_admin.initialize_app(cred)
#_pyrebase = pyrebase.initialize_app(json.load(open("firebase-config.json")))
_pyrebase = pyrebase.initialize_app(json.loads(settings.FIREBASE_CONFIG))
firestore_client = firestore.client()

@router.post("/signup")
async def signup(request: Request):
   client_req = await request.json()
   email = client_req["email"]
   password = client_req["password"]
   if email is None or password is None:
      raise HTTPException(status_code=400, detail="Bad request! Missing email or password!")
   try:
      user = auth.create_user(email=email, password=password)
      return JSONResponse(content=f"User successfully created: id={user.uid}", status_code=202)
   except Exception as ex:
      raise HTTPException(detail=f"Error creating User! Error: {ex}", status_code=400)
   
@router.post("/login")
async def login(request: Request):
   client_req = await request.json()
   email = client_req["email"]
   password = client_req["password"]
   try:
      user = _pyrebase.auth().sign_in_with_email_and_password(email=email, password=password)
      jwt = user["idToken"]
      api_key = get_random_api_key()
      return JSONResponse(content=f"token: {jwt} api_key: {api_key}", status_code=200)
   except Exception as ex:
      raise HTTPException(detail=f"Invalid credentials! Error: {ex}", status_code=400) 

def get_random_api_key() -> str:
   id = random.choice([0, 1, 2])
   docs = firestore_client.collection("keys").stream()
   doc_ids = [doc.id for doc in docs]
   return doc_ids[id]

def create_key(api_key: str):
   firestore_client.collection("keys").document(api_key).set({})


def check_api_key_exist(api_key: str):
   doc = firestore_client.collection("keys").document(api_key).get()
   return doc.exists
