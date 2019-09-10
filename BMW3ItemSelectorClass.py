'''
(PROJECTNAME)ItemSelectorClass Template
This is a template class for accessing and selecting elements on a web page.
METHOD ASSUMPTIONS:
THERE IS A TRY/EXCEPT CLAUSE FOR EVERY SINGLE METHOD!! THIS IS NOT SHOWN FOR EVERY ONE
BUT IT IS IMPLIED! A single function failure should not mean the whole class fails.
Confirmation messages are also implied
The methods are organized into how (I feel) they should be designed based on the element we are interacting with
(button, select, radio button, etc.)
'''

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains as action
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from ErrorHandler import ErrorHandler
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

import time

import time
import random


class SelectItem:

    driver = webdriver
    wait = WebDriverWait
    handler = ErrorHandler

    def __init__(self):
        self.driver = webdriver.Chrome(r"C:\drivers\chromedriver.exe")
        self.wait = WebDriverWait(self.driver, 5)
        self.handler = ErrorHandler()

    def loadtime(self):
        navigationStart = self.driver.execute_script("return window.performance.timing.navigationStart")
        responseStart = self.driver.execute_script("return window.performance.timing.responseStart")
        domComplete = self.driver.execute_script("return window.performance.timing.domComplete")
        # Calculate the performance
        backendPerformance_calc = responseStart - navigationStart
        frontendPerformance_calc = domComplete - responseStart
        print("Back End: %s" % backendPerformance_calc)
        print("Front End: %s" % frontendPerformance_calc)
        return

    def get_to_build(self, model):
        try:
            self.driver.get("https://www.bmwusa.com/build-your-own.html#/series/3/sedan")

            if model == "330i":
                Button330i = self.wait.until(ec.element_to_be_clickable((By.XPATH, "//a[@title='2020 BMW 330i Sedan']")))
                Button330i.click()
            elif model == "330i xDrive":
                print("330i xDrive selected.")
            elif model == "M340i":
                print(model)
            elif model == "M340i xDrive":
                print("M340i xDrive selected.")
            else:
                print("Invalid model")
        except Exception as err:
            self.replug(model)

    # are you "unplugged" from the config? replug!
    def replug(self, model):
        self.get_to_build(model)


'''
begin _ItemSelectorClass:
    define class variables here
    ex: driver = webdriver, wait = WebDriverWait

    define initialization method(self):
        initialize class variables
        ex. self.driver = webdriver.Chrome(chromepath)

    define ItemSelection BUTTON method(self):
        TRY:
            use explicit wait to find the element
            then click using an action chain
            print success message
        EXCEPT:
            print error message

    define ItemSelection SELECT method(self, index): < index arg lets you select a choice from outside the class
        try:
            use explicit wait to find the element
            select the index that is passed as an argument
            print success message
        except:
            print error message

    define ItemSelection RADIO method(self, index)
        try:
            create an if-else statement that selects the radio button based on the index (case-switch works too, probably better)
            i.e.
            if index == 0
                choose radio button option 0 (you will likely need to find this element via label)
                explicit wait doesnt always work here, might have to use a time.sleep
            else if index == 1
                same thing but next label
            else if index == 2
                same thing but next label

            print success message
        except:
            print error message

    define ItemSelection INPUT method(self, text)
        try:
            use explicit wait to find the input element
            use an action chain to click the element, then sendkeys "text"
            print success message
        except:
            print error message
'''