import requests as rq
import pandas as pd
from selenium import webdriver as wd
from bs4 import BeautifulSoup as bs
import re
import time

gdf = pd.read_excel('/home/dynev/Downloads/KAPs_TTDB.xlsx', header=None) #Address
gdf.columns = ['Gene','Species','Strain','ID']
mrnas = []

driver = wd.Firefox()

def get_seq(id, sleep=5):
    driver.get('http://tritrypdb.org/tritrypdb/app/record/gene/%s' % id)
    time.sleep(sleep)
    html = driver.page_source
    soup = bs(html, 'xml')
    soup = soup.text
    try:
        result = re.search(r'Predicted RNA/mRNA Sequence', soup).end()
    except AttributeError as e:
        return 'Error!'
    leap = soup[result:(result+3000)]
    final = re.search(r'((?<=bp)|(?<=bputr))[atgc]*[ATGCN]*[atgc]*(?=Genomic)', leap)
    final = final.group(0)
    final = re.search(r'[ATGCN]+', final)
    final = final.group(0)
    if final is not None:
        return final
    else:
        return 'Error!'

for i in range(5):
    temp = get_seq(gdf.iloc[i]['ID'])
    if temp == 'Error!': 1
        temp = get_seq(gdf.iloc[i]['ID'], 10)
    else:
        mrnas.append(temp)

if ('Error!' not in mrnas) and (len(mrnas)==len(gdf.index)):   
    gdf['mRNA w/o UTR'] = mrnas
    gdf.to_excel('/home/dynev/Downloads/KAPs_full.xlsx', index=None) #Address
