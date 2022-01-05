import pandas as pd
import numpy as np
from urllib.request import urlopen
import time
from selenium import webdriver
import pdftotext
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
import time
import re

#input http address, get element text from h3 and .article-item


start_time = time.time()
print("starting time:",datetime.now())


# run chrome at the backend
chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(executable_path='./chromedriver',options=chrome_options)

# open excel file containing game link
wb = load_workbook(filename='link_per_game.xlsx')
ws = wb["Sheet1"]



# first row become column name
df = pd.DataFrame(ws.values)
df.columns = df.iloc[0, :]
df.drop(df.index[0], inplace=True)
# game_id 125 has an invalid link
df.drop( df.loc[df['game_id'] == 125].index, inplace=True)


# get the info for the first 10 games.
df1 = df.iloc[0:10,].copy()

data = []
timeout = 5

for idx, count in df1.iterrows():


    # read link url from excel
    url = df1.loc[idx, 'link']
    game_id = df1.loc[idx, 'game_id']
    print('game_id:',game_id)
    if url[-3:] != "pdf":
        try:
            driver.get(url)
            # wait
            # get the table on the webpage
            element_present = EC.presence_of_element_located((By.CLASS_NAME, 'tablesaw-cell-content'))
            WebDriverWait(driver, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load id:",str(game_id))


        # for each last-2-min game, find all the comments_element (1 comment per call)
        comments_element = driver.find_elements_by_xpath("//*[text()[contains(.,'Comment:')]]/following-sibling::td")
        #print(len(comments))




        # for each comment (game call) record the details:
        for comment_element in comments_element:

            comment = ILLEGAL_CHARACTERS_RE.sub('@',comment_element.text)

            comment_sibling = comment_element.find_elements_by_xpath("../preceding-sibling::tr[1]/td")


            Period = comment_sibling[0].text
            Time = comment_sibling[1].text
            Call_Type = comment_sibling[2].text
            Committing_Player = comment_sibling[3].text
            Disadvantaged_Player = comment_sibling[4].text
            Review_Decision = comment_sibling[5].text
            Video = comment_sibling[6].text
            #print(Period,Time,Call_Type,Committing_Player,Disadvantaged_Player,Review_Decision,Video)
            data.append([game_id,comment,Period,Time,Call_Type,Committing_Player,Disadvantaged_Player,Review_Decision,Video])

# save data
df = pd.DataFrame(data, columns=['game_id', 'Comment','Period','Time','Call_Type','Committing_Player','Disadvantaged_Player','Review_Decision','Video'])
df.to_excel('referee_mistake.xlsx', sheet_name="Sheet1")

print("--- %s seconds ---" % (time.time() - start_time))
print("end time:", datetime.now())
