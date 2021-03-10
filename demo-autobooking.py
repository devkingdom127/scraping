from bs4 import BeautifulSoup, element
import os
import sys
import time
from threading import Thread
import re
import requests
from sys import platform
from bs4 import BeautifulSoup
from datetime import datetime
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC



BASE_URL = "https://reservations.ontarioparks.com/create-booking/results?resourceLocationId=-2147483600&mapId=-2147483424&searchTabGroupId=0&bookingCategoryId=0&startDate=2021-07-22&endDate=2021-07-23&nights=1&isReserving=true&equipmentId=-32768&subEquipmentId=-32768&partySize=1&searchTime=2021-02-20T10:56:36.407"
driver = webdriver.Chrome()

def main():
   
    driver.get(BASE_URL)
    driver.maximize_window()
    time.sleep(5)
    driver.find_element_by_class_name('mat-checkbox-inner-container').click()
def scrollToElement():
# scroll down to element

    element = driver.find_element_by_id("map")
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()


# select the green spots-605
def Booking():
    now = datetime.now()
    server_url = "https://reservations.ontarioparks.com/api/transactionlocation/servertime"
    r = requests.get(server_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    
    fullSpots = driver.find_elements_by_class_name('legendIconSvg')
    
   
    for fullSpot in fullSpots:
        while True:
            fullSpot.find_element_by_xpath('//div[@id="map"]/div[1]/div[4]/div[219]/*[name()="svg"][@class="legendIconSvg"]').click()  
            time.sleep(10)
            driver.find_element_by_id('addToStay').click()
    driver.close()
 # self.driver.find_element_by_id('mat-dialog-1').click()
                # self.driver.find_element_by_xpath('//*[@id="mat-dialog-1"]/app-reserve-restriction-dialog/div/mat-dialog-actions/button/span[text()="Close"]').click()
                
                # //*[@id="mat-dialog-1"]/app-reserve-restriction-dialog/div/mat-dialog-actions/button/span
if __name__ == '__main__':
    main()
    scrollToElement()
    Booking()
   