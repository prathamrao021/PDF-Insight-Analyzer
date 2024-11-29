from datetime import datetime, time, timezone
# from sqlalchemy import create_engine
from fastapi import FastAPI, Request, UploadFile, File
# from sqlalchemy.orm import Session
# from pydantic import BaseModel, ConfigDict
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
import os
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = './uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.post("/upload_files")
async def upload_file(files: list[UploadFile] = File(...)):
    for file in files:
        file_location = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_location, 'wb') as file_object:
            file_object.write(await file.read())
    return JSONResponse(content={"message": "Files uploaded successfully"})
