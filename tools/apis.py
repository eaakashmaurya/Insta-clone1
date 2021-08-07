from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.support.select import Select 
import re
import requests

def sandhi_api(txt1, txt2):
    
    driver = webdriver.Chrome("/home/piyush/Downloads/chromedriver")
    driver.minimize_window()
    driver.get("http://sanskrit.uohyd.ac.in/scl/")

    tools = driver.find_element_by_xpath('//*[@id="menu"]/li[1]/a')
    actions = ActionChains(driver)
    actions.move_to_element(tools).perform()
    
    driver.implicitly_wait(10)
    splitter = driver.find_element_by_xpath('//*[@id="sandhi-joiner"]')
    splitter.click()

    driver.find_element_by_xpath('//*[@id="text"]').send_keys(txt1)
    driver.find_element_by_xpath('//*[@id="text1"]').send_keys(txt2)
    driver.find_element_by_xpath('//*[@id="submit-sandhi"]').click()

    time.sleep(5)
    result = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="AoutoNumber1"]/tbody/tr[2]/td[3]/center/font')))
    return result.text


def sandhi_splitter_api(txt1, type):
    
    driver = webdriver.Chrome("/home/piyush/Downloads/chromedriver")
    driver.minimize_window()
    driver.get("http://sanskrit.uohyd.ac.in/scl/")

    tools = driver.find_element_by_xpath('//*[@id="menu"]/li[1]/a')
    actions = ActionChains(driver)
    actions.move_to_element(tools).perform()
    
    driver.implicitly_wait(10)
    splitter = driver.find_element_by_xpath('//*[@id="sandhi-splitter"]')
    splitter.click()

    # Select पदच्छेदः
    sandhi_type= Select(driver.find_element_by_xpath('//*[@id="sandhi_type"]'))
    sandhi_type.select_by_visible_text(type)

    driver.find_element_by_xpath('//*[@id="word"]').send_keys(txt1)
    driver.find_element_by_xpath('//*[@id="submit-sandhi"]').click()

    time.sleep(5)

    output_div = driver.find_element_by_xpath('//*[@id="finalout"]')
    result = ""
    first = True
    for word in output_div.find_elements_by_tag_name('a'):
        if (len(word.text) == 0):
            break
        if(not(first)):
            result += " + "
        else:
            first = False
        result += word.text
    return result


def eng_to_sans_api(word):
    url = "https://sanskritdictionary.com/?q=" + word + "&display=devanagari"

    payload={}
    headers = {
    'authority': 'sanskritdictionary.com',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://sanskritdictionary.com/?iencoding=iast&q=bird&lang=sans&action=Search',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7',
    'cookie': '__cfduid=d297f8dcbd0386b680d40d4989cf294f91609240752; PHPSESSID=6383ad43abb377e2e868b973282e8b8a; enabled=1; sansVisitor=XzoGdS4XVX2JFhv4sVGiDIKWU; enabled=1; sansVisitor=ZGs9tx7lM9AUZQdVlyed05Llf'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    ans = response.text.split("<tr style='background: white;'><td width='30%'>")

    if (len(ans) > 1):
        ans = ans[1].split(">")
        if (len(ans) > 1):
            return ans[1].split("<")[0]

    return "Not Found"

def sans_to_eng_api(word):
    url = "https://sanskritdictionary.com/?iencoding=iast&q=" + word + "&lang=sans&action=Search"

    payload={}
    headers = {
    'authority': 'sanskritdictionary.com',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://sanskritdictionary.com/?iencoding=iast&q=%E0%A4%A6%E0%A5%87%E0%A4%B9&lang=sans&action=Search',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7',
    'cookie': '__cfduid=d297f8dcbd0386b680d40d4989cf294f91609240752; PHPSESSID=6383ad43abb377e2e868b973282e8b8a; enabled=1; sansVisitor=XzoGdS4XVX2JFhv4sVGiDIKWU; enabled=1; sansVisitor=ZGs9tx7lM9AUZQdVlyed05Llf'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    ans = response.text.split("</td><td width='50%'>")
    if (len(ans) > 1):
        ans = ans[1].split("</b>")
        if (len(ans) > 1):
            return re.sub(r'[^A-Za-z0-9 ]+', '', ans[1].split("<")[0])
        else:
            return re.sub(r'[^A-Za-z0-9 ]+', '', ans[0].split("<")[0])
    return "Not Found"
