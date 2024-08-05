from bs4 import BeautifulSoup
import re
import requests
from concurrent.futures import ThreadPoolExecutor
import time
import csv
import json
import os
from datetime import datetime
start_time = time.time()
url='http://backrooms-wiki.wikidot.com/entities'



stranka = requests.get(url)
doc = BeautifulSoup(stranka.text , "html.parser")


levels_block = doc.find_all('div', class_='yui-content')
levels_block = levels_block[-1]
itemy = levels_block.find_all('li')
url_name = []

for item in itemy:
    # Split the text and process each part
    parts = item.get_text().split(' - ', 1)
    
    # Extract quoted text if present
    if len(parts) > 1:
        second_element = parts[1]
        quoted_text = re.search(r'"[^"]*"', second_element)
        if quoted_text:
            parts[1] = quoted_text.group(0)
            parts[1] = parts[1][1:-1]
    else:
        parts.append(None)
        
    
    # Append processed parts to the list
    url_name.append(parts)


def akcia(item): 

    stranka = None  
    doc = None
    
    if item[0] == 'SPLIT(!)HEAD IS A FLAGGED TERM!':
        item[0] ='entity-500'
        
    try:
        if item[1] == "[NO DATA]":
            rating = None
            tags = None
            url_adresa = None
            rating_tags = (rating,tags , url_adresa) 
            item.extend(rating_tags)
            return
    except:
        pass
    
    x = 4
    time.sleep(0.11)
    for i in range(7):
        try:
            url_adresa = f'http://backrooms-wiki.wikidot.com/{item[0]}'
            stranka = requests.get(url_adresa)
            doc = BeautifulSoup(stranka.text , "html.parser")
            x = 7
        except:
            if i ==6:
                print(f'NENACITALA SA STRANKA PRE {item[0]}')
            
            
        if x == 7:
            break
        
    if stranka is None:
        return
    
    try:
        rating = doc.find('span', id='prw54355').get_text()
    except:
        print(f'pre {item[0]} sa rating rating nenasiel')
    
    
    tags = []
    try:
        tags_html = doc.find('div', class_='page-tags').find('span').find_all('a')
        for tag in tags_html:
            tag_text = tag.get_text()
            tags.append(tag_text)
        
        rating_tags = (rating,tags , url_adresa) 
        item.extend(rating_tags)
    except:
        print(f'pre {item[0]} sa tags rating nenasiel')

with ThreadPoolExecutor(max_workers=60) as p:
    p.map(akcia ,url_name)

with open('data/backrooms_entities.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Level', 'Name', 'Rating', 'Tags' , 'Url'])
    writer.writerows(url_name)


end_time_scraping = time.time()
print(f"Scraping time: {end_time_scraping - start_time} seconds")

start_time_pandas = time.time()


import pandas as pd
df = pd.read_csv('data/backrooms_entities.csv')
df =df[df['Name'] !='[NO DATA]']

analyzed_file_path = 'data/backrooms_entities_analyzed.csv'
if os.path.isfile(analyzed_file_path):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    new_analyzed_file_path = f'data/backrooms_entities_analyzed_{timestamp}.csv'
    os.rename(analyzed_file_path, new_analyzed_file_path)
    df.to_csv(analyzed_file_path, index=False)
else:
    df.to_csv(analyzed_file_path, index=False)

end_time_pandas = time.time()
print(f"Pandas time: {end_time_pandas - start_time_pandas} seconds")


start_time_gsheet = time.time()


import gspread
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np

scope = ["https://spreadsheets.google.com/feeds", 
         "https://www.googleapis.com/auth/drive"]


creds = ServiceAccountCredentials.from_json_keyfile_name('random-project-420514-74ed8d01ffb1.json', scopes=scope)
client = gspread.authorize(creds)
sheet_id = '1muMkOmtZQM959YOTOdGSjQek0Z_mPHB-qZHdxoDHo34'
sheet = client.open_by_key(sheet_id)


databaza = sheet.get_worksheet(1)
databaza.clear()

csv_file_path = 'data/backrooms_entities_analyzed.csv'
df = pd.read_csv(csv_file_path)


df = df.replace({np.nan: '', np.inf: 1e10, -np.inf: -1e10})
df_list = [df.columns.values.tolist()] + df.values.tolist()
databaza.update(df_list)

end_time_gsheet = time.time()

print(f"Gsheet time: {end_time_gsheet - start_time_gsheet} seconds")

print(f"Total time: {end_time_gsheet - start_time} seconds")