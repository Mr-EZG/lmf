# __author__ = "Ethan Garza"

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import numpy as np
import json

zillow_url_base = "https://www.zillow.com"
zillow_agent_reviews_url = "real-estate-agent-reviews/"

# This follows Google's general query format, the search is at the end of the query
driver = webdriver.Chrome(ChromeDriverManager().install())

#

# Xpath lists (for buttons and interacting with webpage, etc)

# search parameters for zillow
places = ['austin-tx','san_antonio-tx','omaha-ne', 'cambridge-ma', 'somerville-ma'] # Can be city / state or by zip

# This block is for contacting agents to sell a home and/or buy a home
all_inputs = True
buying_home = True
selling_home = True

x_path_list = []
overall_info = dict()

test_company = ['united airlines']
# test_time = [ytd_btn_xpath]

for place in places:
    driver.get(zillow_url_base + "/" + place + "/" + zillow_agent_reviews_url)

driver.quit()

# print("Loading into a file...")
# np.save("transportation_data.npy", overall_info)
# print("--------")
# print("Stuff:")
# print(overall_info)
# json.dump(overall_info, open("text.txt",'w'))