from selenium import webdriver
from selenium.webdriver import Chrome
import time 
from bs4 import BeautifulSoup
import csv


Scroll_pause_time = 1
count=1 


driver = webdriver.Chrome("~/Downloads/chromedriver_mac_arm64") #accessing the browser
driver.get("https://www.reddit.com/r/selfhosted/top/?t=all")
time.sleep(2)
last_height = driver.execute_script("return window.screen.height;")#returns the height of the screen

#Loop for scrolling down the page
while True:
    driver.execute_script("window.scrollTo(0, {last_height} * {i});".format(last_height=last_height, i=count))
    count+=1
    time.sleep(Scroll_pause_time)
    new_height = driver.execute_script("return document.body.scrollHeight;")
    #if the next iteration(i.e. next scroll) doesn't happen, the loop breaks 
    if last_height * count > new_height:
        break

#Scrapping of required data(i.e. title and time of post) 
soup = BeautifulSoup(driver.page_source, 'html.parser')
period = soup.div.find_all("span",attrs={"class" : "_2VF2J19pUIMSLJFky-7PEI"})
title = soup.div.find_all("h3",attrs={"class" : "_eYtD2XCVieq6emjKBH3m"})


#Exporting the data into CSV
with open("self_hosted.csv","w",newline = "") as file:
    wr = csv.writer(file)
    rows = ["Title","Time"]
    wr.writerow(rows)
    for i in range(15):
        rw = [title[i].text,period[i].text]
        wr.writerow(rw)

