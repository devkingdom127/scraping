from bs4 import BeautifulSoup, element
import os
import sys
import time
from threading import Thread
import re
import requests
import dateparser
import datetime as DT
from sys import platform
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from threading import Thread
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


DESTINATION = "Killbear Provincial Park"
T2 = 'T12:00:00.0000000Z'
def init_chrome_driver():
    directory = os.path.abspath(os.path.dirname(__file__))
    if os.name == 'nt':
        chrome_driver = '\chromedriver.exe'
    else:
        sys.exit('Program works on windows only.')
    driver = webdriver.Chrome(directory + chrome_driver)
    driver.maximize_window()
    return driver

class AutoBooking:
    def __init__(self, url):
        self.url = url
        self.driver = init_chrome_driver()

        self.now = datetime.now()
        self.day = self.now.strftime('%d')
        self.month = self.now.strftime('%m')
        self.year = self.now.strftime('%Y')

        pst_dt = dateparser.parse(str(self.now ))
        utc_dt = pst_dt.astimezone(DT.timezone.utc)
        print("----------------PST Time Now-------------------", pst_dt)
        print("----------------UTC Time Now-------------------", utc_dt)
        
        try:
            self.driver.get(self.url)
            
        except:
            self.driver.quit()
            sys.exit('Invalid URL address.')
    
    def quit_driver(self):
        self.driver.quit()

    def take_screenshot(self):
        self.driver.save_screenshot('screenshot.png')
    
    def booking(self):
        
        # self.driver.find_element_by_xpath('//div[@id="map"]/div[1]/div[4]/div[123]/*[name()="svg"][@class="legendIconSvg"]').click()
        # //*span[@class = 'mat-button-wrapper']".text();
        # //*[@id="consentButton"]/span
        # //*[@id="acknowledgement"]/label/div
        self.driver.find_element_by_id("consentButton").click()
        print("--------------------click I consent-----------------")
        time.sleep(10)
        self.driver.find_element_by_class_name('mat-checkbox-inner-container').click()
        # self.driver.find_element_by_id("acknowledgement").click()
       
        element = self.driver.find_element_by_id("map")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()

        time.sleep(5)
    
        server_url = "https://reservations.ontarioparks.com/api/transactionlocation/servertime"
        r = requests.get(server_url)
        serverTime = BeautifulSoup(r.content, 'html.parser')

        print("-------------Server Time-----------------", serverTime)
       
        T1 = str(serverTime).split("T")[1]
        print('-----------------T1---------------------', T1)
        # time.sleep(5)

        # fullSpots = self.driver.find_elements_by_class_name('site-label-text')
        fullSpots = self.driver.find_elements_by_class_name('legendIconSvg')
        
        for fullSpot in fullSpots:
            
        
            # fullSpot.find_element_by_xpath('//div[@id="map"]/div[1]/div[4]/div[219]/*[name()="svg"][@class="legendIconSvg"]').click()  
            fullSpot.find_element_by_xpath('//div[@id="map"]/div[1]/div[4]/div[123]/*[name()="svg"][@class="legendIconSvg"]').click()
            print('-------------------------------------------------click greenspot-------------------------------------------------')
            element = self.driver.find_element_by_id("map")
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()
            time.sleep(5)
            while True:
                self.driver.find_element_by_id('addToStay').click()

                time.sleep(5)
               
                self.driver.find_element_by_xpath('//*[@id="mat-dialog-0"]/app-reserve-restriction-dialog/div/mat-dialog-actions/button/span').click()
                print('---------Click close button-----------------------')
        self.driver.close()      

if __name__ == '__main__':
    
    try:
        # wp = AutoBooking('https://reservations.ontarioparks.com/')
        
        wp = AutoBooking('https://reservations.ontarioparks.com/create-booking/results?resourceLocationId=-2147483600&mapId=-2147483426&searchTabGroupId=0&bookingCategoryId=0&startDate=2021-07-24&endDate=2021-07-25&nights=1&isReserving=true&equipmentId=-32768&subEquipmentId=-32768&partySize=1&searchTime=2021-02-22T03:44:46.464')                
        wp.booking()
        # wp.get_serverTime()
        wp.quit_driver()
        
        sys.exit(0)
    except KeyboardInterrupt:
        sys.exit(1)
