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
import random

# <html>
#  <head>
#   <meta content="noindex, nofollow" name="robots"/>
#   <link href="https://www.zillowstatic.com/vstatic/80d5e73/static/css/z-pages/captcha.css" media="screen" rel="stylesheet" type="text/css"/>
#   <script>
#    window._pxAppId = 'PXHYx10rg3';
#         window._pxJsClientSrc = '/HYx10rg3/init.js';
#         window._pxHostUrl = '/HYx10rg3/xhr';
#         window._pxFirstPartyEnabled = true;
#         window._pxreCaptchaTheme='light';
#   </script>
#   <script src="https://captcha.px-cdn.net/PXHYx10rg3/captcha.js?a=c&amp;m=0" type="text/javascript">
#   </script>
#   <script>
#    function getQueryString(name, url) {
#             if (!url) url = window.location.href;
#             name = name.replace(/[\[\]]/g, "\\$&");
#             var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
#                 results = regex.exec(url);
#             if (!results) return null;
#             if (!results[2]) return '';
#             return decodeURIComponent(results[2].replace(/\+/g, " "));
#         }
#         document.addEventListener("DOMContentLoaded", function(e) {
#             var uuidVerifyRegExp = /^\{?[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\}?$/i;
#             document.getElementById("uuid").innerText = "UUID: " + uuidVerifyRegExp.exec(getQueryString("uuid"));
#         });
#
#         function handleCaptcha(response) {
#             var vid = getQueryString("vid"); // getQueryString is implemented below
#             var uuid = getQueryString("uuid");
#             var name = '_pxCaptcha';
#             var cookieValue =  btoa(JSON.stringify({r:response,v:vid,u:uuid}));
#             var cookieParts = [name, '=', cookieValue, '; path=/'];
#             cookieParts.push('; domain=' + window.location.hostname);
#             cookieParts.push('; max-age=10');//expire after 10 seconds
#             document.cookie = cookieParts.join('');
#             var originalURL = getOriginalUrl("url");
#             var originalHost = window.location.host;
#             var newHref = window.location.protocol + "//" + originalHost;
#             originalURL = originalURL || '/';
#             newHref = newHref + originalURL;
#             window.location.href = newHref;
#         }
#
#         function getOriginalUrl(name) {
#             var url = getQueryString(name);
#             if (!url) return null;
#             var regExMatcher = new RegExp("(([^&#@]*)|&|#|$)");
#             var matches = regExMatcher.exec(url);
#             if (!matches) return null;
#             return matches[0];
#         }
#   </script>
#  </head>
#  <body>
#   <main class="zsg-layout-content">
#    <div class="error-content-block">
#     <div class="error-text-content">
#      <!-- <h1>Captcha</h1> -->
#      <h5>
#       Please verify you're a human to continue.
#      </h5>
#      <div class="captcha-container" id="content"> **********************************************************************
#       <div data-callback="handleCaptcha" id="px-captcha">
#       </div>
#       <img alt="Zillow" height="14" src="https://www.zillowstatic.com/static/logos/logo-65x14.png" width="65"/>
#      </div>
#     </div>
#    </div>
#   </main>
#   <h4 class="uuid-string zsg-fineprint" id="uuid">
#   </h4>
#  </body>
# </html>
zillow_url_base = "https://www.zillow.com"
zillow_agent_reviews_url = "real-estate-agent-reviews/"
zillow_page_suffix = "?page="
headers_list = [
    # Firefox 77 Mac
     {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.google.com/",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    },
    # Firefox 77 Windows
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.google.com/",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    },
    # Chrome 83 Mac
    {
        "Connection": "keep-alive",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://www.google.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
    },
    # Chrome 83 Windows
    {
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://www.google.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9"
    }
]

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

# X paths
x_path_list = []
overall_info = dict()

# agent_name to relative url
agents_to_contact = {}

def handle_captcha(driver):
    while True:
        if not driver.find_element_by_class_name('captcha-container').is_displayed():
            break


for place in places:
    agents_to_contact[place] = {}
    for i in range(1, 2):
        agents_to_contact[place][i] = {}

for place in places:
    # was 1 to 15
    for i in range(1, 2):
        driver.header_overrides = random.choice(headers_list)
        driver.get(zillow_url_base + "/" + place + "/" + zillow_agent_reviews_url+zillow_page_suffix + str(i))
        #Attempt to handle captcha
        try:
            captcha = driver.find_element_by_class_name('captcha-container').is_displayed()
            if captcha :
                print("We got a captcha")
                handle_captcha(driver)
        except Exception as e:
            pass
        time.sleep(2)
        content = driver.page_source
        soup = BeautifulSoup(content, features='lxml', )
        all_listings = soup.find('div', attrs={'class': 'ldb-boards-results'})
        sup = all_listings.find_all('div', attrs={'class': 'zsg-separator ldb-table ldb-table-abc ldb-fg-bg-container za-track-event'})
        # due to ten listings per page
        # was 1 to 10
        # print("sup:", sup)
        for j in range(0, 10):
            agent_name = sup[j].find('p', attrs={'class': 'ldb-contact-name ldb-font-bold'})
            # print("agent name:", agent_name)
            relative_url = agent_name.find('a')['href']
            # print("relative url:", relative_url)
            agents_to_contact[place][i][agent_name.text] = relative_url

print(agents_to_contact)
name_box_xpath = "/html/body/div[1]/div[7]/aside/div/section[1]/div/section/form/ul[1]/li[1]"
name_box_xpath = "/html/body/div[1]/div[7]/aside/div/section[1]/div/section/form/ul[1]/li[1]/input"
name_box_xpath2 = "/html/body/div[1]/div[7]/aside/div/section[2]/div/section/form/ul[1]/li[1]/input"

phone_xpath = "/html/body/div[1]/div[7]/aside/div/section[1]/div/section/form/ul[1]/li[2]"
phone_xpath = "/html/body/div[1]/div[7]/aside/div/section[1]/div/section/form/ul[1]/li[2]/input"
phone_xpath2 = "/html/body/div[1]/div[7]/aside/div/section[2]/div/section/form/ul[1]/li[2]/input"

email_xpath = "/html/body/div[1]/div[7]/aside/div/section[1]/div/section/form/ul[1]/li[3]"
email_xpath = "/html/body/div[1]/div[7]/aside/div/section[1]/div/section/form/ul[1]/li[3]/input"
email_xpath2 = "/html/body/div[1]/div[7]/aside/div/section[2]/div/section/form/ul[1]/li[3]/input"

message_xpath = "/html/body/div[1]/div[7]/aside/div/section[1]/div/section/form/ul[1]/li[4]"
message_xpath = "/html/body/div[1]/div[7]/aside/div/section[1]/div/section/form/ul[1]/li[4]/textarea"
message_xpath2 = "/html/body/div[1]/div[7]/aside/div/section[2]/div/section/form/ul[1]/li[4]/textarea"


submit_btn_xpath = "/html/body/div[1]/div[7]/aside/div/section[1]/div/section/form/ul[2]/li/button"
submit_btn_xpath2 = "/html/body/div[1]/div[7]/aside/div/section[2]/div/section/form/ul[2]/li/button"

sender_name = "I was Here XD"
phone_number = "123-456-7891"
email = "bruh@gmail.com"
message = "wasssap"



for place in places:
    for i in range(1, 2):
        for agent in agents_to_contact[place][i].keys():
            url = zillow_url_base + agents_to_contact[place][i][agent]
            driver.header_overrides = random.choice(headers_list)
            driver.get(url)
            time.sleep(2)
            #Attempt to handle captcha
            try:
                captcha = driver.find_element_by_class_name('captcha-container').is_displayed()
                if captcha:
                    print("We got a captcha")
                    handle_captcha(driver)
            except Exception as e:
                pass


            try:
                name_box = driver.find_element_by_xpath(name_box_xpath)
                name_box.send_keys(sender_name)
            except Exception as e:
                #Note: not the way to handle this but since I only only found
                #one alternate xpath we should not need a try catch here
                name_box = driver.find_element_by_xpath(name_box_xpath2)
                name_box.send_keys(sender_name)
                pass

            try:
                phone_number_box = driver.find_element_by_xpath(phone_xpath)
                phone_number_box.send_keys(phone_number)
            except Exception as e:
                #Note: not the way to handle this but since I only only found
                #one alternate xpath we should not need a try catch here
                phone_number_box = driver.find_element_by_xpath(phone_xpath2)
                phone_number_box.send_keys(phone_number)
                pass

            try:
                email_box = driver.find_element_by_xpath(email_xpath)
                email_box.send_keys(email)
            except Exception as e:
                #Note: not the way to handle this but since I only only found
                #one alternate xpath we should not need a try catch here
                email_box = driver.find_element_by_xpath(email_xpath2)
                email_box.send_keys(email)
                pass

            try:
                message_box = driver.find_element_by_xpath(message_xpath)
                message_box.send_keys(message)
            except Exception as e:
                #Note: not the way to handle this but since I only only found
                #one alternate xpath we should not need a try catch here
                message_box = driver.find_element_by_xpath(message_xpath2)
                message_box.send_keys(message)
                pass

            try:
                submit_btn = driver.find_element_by_xpath(submit_btn_xpath)
                submit_btn.click()

            except Exception as e:
                #Note: not the way to handle this but since I only only found
                #one alternate xpath we should not need a try catch here
                submit_btn = driver.find_element_by_xpath(submit_btn_xpath2)
                submit_btn.click()
                pass



            # phone_number_box = driver.find_element_by_xpath(phone_xpath)
            # phone_number_box.send_keys(phone_number)
            #
            # email_box = driver.find_element_by_xpath(email_xpath)
            # email_box.send_keys(email)
            #
            # message_box = driver.find_element_by_xpath(message_xpath)
            # message_box.send_keys(message)

            # submit_btn = driver.find_element_by_xpath(submit_btn_xpath)
            # submit_btn.click()

driver.quit()


# print("Loading into a file...")
# np.save("transportation_data.npy", overall_info)
# print("--------")
# print("Stuff:")
# print(overall_info)
# json.dump(overall_info, open("text.txt",'w'))
