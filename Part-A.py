import requests
import sqlite3
import urllib.request
from ast import literal_eval
import json
import pandas as pd

conn=sqlite3.connect('new.db')
c=conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users(id TEXT,title TEXT,firstName TEXT,lastname TEXT,picture TEXT)''')
API_KEY ='626bb2d62735f577c90b3752'

url=('https://dummyapi.io/data/v1/user')
response = requests.get(url,
        headers={
            "app-id":API_KEY,
            "content-type":"application/json"
        })

r = response.json()
for d in range(1,20):
    id=r["data"][d]['id']
    title=r["data"][d]['title']
    firstName=r["data"][d]['firstName']
    lastName=r["data"][d]['lastName']
    picture=r["data"][d]['picture']
    c.execute('''INSERT INTO users VALUES(?,?,?,?,?)''',(id,title,firstName,lastName,picture))


c.execute("select id from users")
for customer in c.fetchall():
    id=customer[0]
    id=id.replace('(\'','')
    id=id.replace('\',)','')
    url=('https://dummyapi.io/data/v1/user/{}/post'.format(id))
    response = requests.get(url,
        headers={
            "app-id":API_KEY,
            "content-type":"application/json"
        })
    r=response.json()
    print(r)


conn.close()