#!/usr/bin/env python3

from fastapi import FastAPI
import MySQLdb
# from typing import Optional
# from pydantic import BaseModel
import mysql.connector
from chalice import Chalice
from mysql.connector import Error
import json
import os
import boto3

app = Chalice(app_name="app.py")
app.debug = True

S3_BUCKET = 'dpv8cf-dp1-spotify'
s3=boto3.client('s3')

DBUSER = os.getenv('DBUSER')
DBHOST = os.getenv('DBHOST')
DBPASS = os.getenv('DBPASS')

DB = "dpv8cf"

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/asd")  # zone apex
def zone_apex():
    return {"Good Day": "Sunshine!"}

@app.get('/genres')
async def get_genres():
    db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB, ssl_disabled=True)
    cur = db.cursor()
    query = "SELECT * FROM genres ORDER BY genreid;"
    try:    
        cur.execute(query)
        headers=[x[0] for x in cur.description]
        results = cur.fetchall()
        json_data=[]
        for result in results:
            json_data.append(dict(zip(headers,result)))
        # cur.close()
        db.close()
        return(json_data)
    except Error as e:
        print("MySQL Error: ", str(e))
        # cur.close()
        db.close()
        return {"Error": "MySQL Error: " + str(e)}



@app.get('/songs')
async def get_genres():
    db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB, ssl_disabled=True)
    cur = db.cursor()
    query = "SELECT songs.title, songs.album, songs.artist, songs.year, songs.file, songs.image, genres.genre FROM songs JOIN genres WHERE songs.genre = genres.genreid;"
    try:
        cur.execute(query)
        headers=[x[0] for x in cur.description]
        results = cur.fetchall()
        json_data=[]
        for result in results:
            json_data.append(dict(zip(headers,result)))
        cur.close()
        db.close()
        return(json_data)
    except Error as e:
        print("MySQL Error: ", str(e))
        cur.close()
        db.close()
        return None