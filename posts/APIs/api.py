from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image
import os

def eng_to_sans(word):
    url = "https://sanskritdictionary.com/?q=" + word + "&display=devanagari"
    driver = webdriver.Chrome("/home/piyush/Downloads/chromedriver")
    driver.minimize_window()
    driver.get(url)

    result = driver.find_element_by_xpath('/html/body/table[1]/tbody/tr[5]/td[2]/table/tbody/tr/td/div/table/tbody/tr[3]/td[1]')
    return result.text

def objDetect(file):
    classNames= []
    classFile = 'posts/APIs/coco.names'
    with open(classFile,'rt') as f:
        classNames = f.read().rstrip('\n').split('\n')

    configPath = 'posts/APIs/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
    weightsPath = 'posts/APIs/frozen_inference_graph.pb'

    net = cv2.dnn_DetectionModel(weightsPath, configPath)
    net.setInputSize(320,320)
    net.setInputScale(1.0/ 127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)

    img = cv2.imread("media/"+file)

    classIds, confs, bbox = net.detect(img,confThreshold=0.5)
    print(classIds,bbox)

    objs = []

    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            cv2.rectangle(img,box,color=(0,255,0),thickness=2)
            cv2.putText(img,classNames[2*classId-2].upper(),(box[0]+10,box[1]+30),
                            cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
            fontpath = "posts/APIs/ARIALUNI.TTF"
            font = ImageFont.truetype(fontpath, 32)
            img_pil = Image.fromarray(img)
            draw = ImageDraw.Draw(img_pil)
            draw.text((box[0]+10,box[1]+30), eng_to_sans(classNames[2*classId-2]), font=font, fill=(255,255,255))
            objs.append(classNames[2*classId-1])
            img = np.array(img_pil)

    cv2.imwrite("media/"+file, img)
    return objs

def get_text(file):
    
    driver = webdriver.Chrome("/home/piyush/Downloads/chromedriver")
    driver.get("https://ocr.sanskritdictionary.com/#")
    driver.find_element_by_id("pictureFile").send_keys(os.getcwd() + "/media/" + file)

    time.sleep(15)
    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="tinymcetext_ifr"]'))
    result = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tinymce"]/p')))
    return result.text

# file = "lena.png"
# objDetect(file)

# file = "/home/piyush/Desktop/Productathon/ObjectDetecter/dipu.png"
# print(get_text(file))
