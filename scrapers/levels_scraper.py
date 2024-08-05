
from bs4 import BeautifulSoup
import re
import requests
from concurrent.futures import ThreadPoolExecutor
import time
import csv
import json
from datetime import datetime
import os

start_time = time.time()
url='http://backrooms-wiki.wikidot.com/normal-levels-i'



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
    if item[0] == 'Paradise 770':
        item[0] ='level-770'
    
    if item[0] == 'Unnamed':
        item[0] ='level-621'
    
    if item[0] == 'Aster':
        item[0] ='level-599'
    
    if item[0] == 'Ground 522.1':
        item[0] ='level-522-1'
    
    if item[0] == '1D4C5..1D505 : a machine that hates':
        item[0] ='level-505'
        
    if item[0] == 'Ground 486':
        item[0] ='level-486'
    
    if item[0] == 'Paradise 451':
        item[0] ='level-451'
    
    if item[0] == 'The Sanctum Subterraneous':
        item[0] ='the-sanctum'
    
    if item[0] == 'Asset 11.1':
        item[0] ='level-11-1'
    
    if item[0] == 'Scene-01.2':
        item[0] ='level-11-2'
    
    if item[0] == 'Ground 46.1':
        item[0] ='level-46-1'
    
    if item[0] == 'Ground 48.1':
        item[0] ='level-48-1'
    
    if item[0] == 'bHZsMzUy':
        item[0] ='level-352'
    
    if item[0] == 'Level ʡ':
        item[0] ='level-262'
    
    if item[0] == 'You cheated.':
        item[0] ='level-363'
    
    
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

with open('data/backrooms_levels.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Level', 'Name', 'Rating', 'Tags' , 'Url'])
    writer.writerows(url_name)


end_time_scraping = time.time()

# Print the elapsed time
print(f"Scraping time: {end_time_scraping - start_time} seconds")

start_time_pandas = time.time()

import pandas as pd
df = pd.read_csv('data/backrooms_levels.csv')

class_tags = [
    'sd-class-?', 'sd-class-0', 'sd-class-1', 'sd-class-2', 'sd-class-3', 
    'sd-class-4', 'sd-class-5', 'sd-class-deadzone', 'sd-class-habitable', 
    'sd-class-other', 'sd-class-pending'
]

# Function to find the class in tags
def find_class(tags):
    if pd.isna(tags):
        return None
    for tag in class_tags:
        if tag in tags:
            return tag
    return None

# Apply the function to the Tags column and create the Class column
df['Class'] = df['Tags'].apply(find_class)
cols = list(df.columns)
cols.insert(3, cols.pop(cols.index('Class')))
df = df[cols]
df =df[df['Name'] !='[NO DATA]']

analyzed_file_path = 'data/backrooms_levels_analyzed.csv'
if os.path.isfile(analyzed_file_path):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    new_analyzed_file_path = f'data/backrooms_levels_analyzed_{timestamp}.csv'
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


databaza = sheet.get_worksheet(0)
databaza.clear()

csv_file_path = 'data/backrooms_levels_analyzed.csv'
df = pd.read_csv(csv_file_path)


df = df.replace({np.nan: '', np.inf: 1e10, -np.inf: -1e10})
df_list = [df.columns.values.tolist()] + df.values.tolist()
databaza.update(df_list)

end_time_gsheet = time.time()

print(f"Gsheet time: {end_time_gsheet - start_time_gsheet} seconds")

print(f"Total time: {end_time_gsheet - start_time} seconds")
