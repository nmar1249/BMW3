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


    def select_model(self, model):
        try:
            self.driver.get("https://www.bmwusa.com/build-your-own.html#/series/3/sedan")

            models = {
                0: "//a[@title='2020 BMW 330i Sedan']",
                1: "//a[@title='2020 BMW 330i xDrive Sedan']",
                2: "//a[@title='2020 BMW M340i Sedan']",
                3: "//a[@title='2020 BMW M340i xDrive Sedan']"
            }
            self.loadtime()

            button = self.wait.until(
                ec.element_to_be_clickable((By.XPATH, models.get(model, "invalid index"))))
            button.click()
            print("Model selected. Index: " + str(model))

        except Exception as err:
            print(str(err))
            self.replug(model)

    # are you "unplugged" from the config? replug!
    def replug(self, model):
        self.select_model(model)

    # select Design - 330i
    def select_design_330i(self, index):
        try:
            self.loadtime()

            designs = {
                0: "//div[@title='Sport Line']",
                1: "//div[@title='Luxury']",
                2: "//div[@title='M Sport']"
            }

            design = self.wait.until(
                ec.element_to_be_clickable((By.XPATH, designs.get(index, "invalid index")))
            )
            design.click()
            print("Design selected. Index: " + str(index))
            self.next_page()
            self.confirm_change()
        except Exception as err:
            self.handler.error_message("330i - design", err)

    def select_color_330i(self, index):
        try:

            colors = {
                0: "//div[@title='Alpine White']",
                1: "//div[@title='Jet Black']",
                2: "//div[@title='Black Sapphire Metallic']",
                3: "//div[@title='Melbourne Red Metallic']",
                4: "//div[@title='Glacier Silver Metallic']",
                5: "//div[@title='Mineral White Metallic']",
                6: "//div[@title='Mineral Grey Metallic']",
                7: "//div[@title='Mediterranean Blue Metallic']",
                8: "//div[@title='Sunset Orange Metallic']",
                9: "//div[@title='Vermont Bronze Metallic']",
                10: "//div[@title='Portimao Blue Metallic']",
                11: "//div[@title='Blue Ridge Mountain Metallic']"
            }

            self.loadtime()
            self.close_zip()
            time.sleep(2)
            color = self.driver.find_element_by_xpath(colors.get(index, "invalid index"))
            self.driver.execute_script("arguments[0].scrollIntoView();", color)
            time.sleep(2)
            color.click()
            self.confirm_change()
            print("Color selected. Index: " + str(index))
        except Exception as err:
            self.handler.error_message("color selection", err)

    def next_page(self):
        try:
            next = self.wait.until(
                ec.element_to_be_clickable((By.CLASS_NAME, "button-next.byo-core-type.label-1.theme-core"))
            )
            next.click()
        except Exception as err:
            self.handler.error_message("moving to next page", err)

    def confirm_change(self):
        try:
            time.sleep(3)
            confirm = self.driver.find_element_by_xpath("//button[@name='confirm-button']")
            confirm.click()
            print("change confirmed!")
        except Exception as err:
            self.handler.error_message("no changes to confirm", err)

    # closes zipcode window - can cause click intercepts if open
    def close_zip(self):
        try:
            time.sleep(2)
            close = self.driver.find_element_by_xpath("//button[@aria-label='Close Zipcode Modal']")
            close.click()
        except Exception as err:
            self.handler.error_message("closing zip modal", err)
