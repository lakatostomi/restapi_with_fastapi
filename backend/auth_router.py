from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from config import settings

router = APIRouter()

from firebase_admin import auth, credentials
import pyrebase
import firebase_admin
import json

cred = credentials.Certificate(settings.FIREBASE_AUTH_SA_KEY)
firebase = firebase_admin.initialize_app(cred)
_pyrebase = pyrebase.initialize_app(json.load(open("firebase-config.json")))
#_pyrebase = pyrebase.initialize_app(settings.FIREBASE_CONFIG)

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
      return JSONResponse(content=f"token: {jwt}", status_code=200)
   except Exception as ex:
      raise HTTPException(detail=f"Invalid credentials! Error: {ex}", status_code=400) 