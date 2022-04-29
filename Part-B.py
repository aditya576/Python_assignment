import re
import urllib.request
from bs4 import BeautifulSoup as bs
import sqlite3

conn=sqlite3.connect('new.db')

c=conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS books(Name TEXT,Price TEXT,Availability TEXT, Rating INT)''')
names=[]
prices=[]
availability=[]
ratings=[]
for page in range(1,51):
    url="http://books.toscrape.com/catalogue/page-{}.html".format(page)
    page=urllib.request.urlopen(url)
    soup=bs(page)

    
    for x in soup.find_all('img'):
        name=x.get('alt')
        names.append(name)

    for a in soup.findAll('li',attrs={'class':'col-xs-6 col-sm-4 col-md-3 col-lg-3'}):
        price=a.find('p',attrs={'class':'price_color'})
        availablity_status=a.find('p',attrs={'class':'instock availability'})
        prices.append(price.text)
        availability.append(availablity_status.text)

    for a in soup.find_all('p'):
        r=a.get('class')
        if len(r)!=2:
            continue
        if r[0]!='star-rating':
            continue
        rating=r[1]
        rating=rating.replace("star-rating ","")
        if rating=="One":
            rating=1
        elif rating=="Two":
            rating=2
        elif rating=="Three":
            rating=3
        elif rating=="Four":
            rating=4
        elif rating=="Five":
            rating=5
        ratings.append(rating)



for i in range(0,len(availability)):
    availability[i]=availability[i].replace("  ","")
    availability[i]=availability[i].replace("\n","")

for i in range(0,len(names)):
   c.execute('''INSERT INTO books VALUES(?,?,?,?)''',(names[i],prices[i],availability[i],ratings[i]))


conn.commit()
c.execute('''SELECT * FROM books''')
results=c.fetchall()
print(results)

conn.close()
