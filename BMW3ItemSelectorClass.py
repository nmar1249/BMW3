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
                0: "//a[@title='2020 BMW 330i Sedan']",         # 330i
                1: "//a[@title='2020 BMW 330i xDrive Sedan']",  # 330i xDrive
                2: "//a[@title='2020 BMW M340i Sedan']",        # M340i
                3: "//a[@title='2020 BMW M340i xDrive Sedan']"  # M340i xDrive
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
            self.driver.execute_script("arguments[0].scrollIntoView();", color)             # GET ELEMENT INTO VIEW
            time.sleep(2)
            color.click()
            self.confirm_change()
            self.next_page()
            print("Color selected. Index: " + str(index))
        except Exception as err:
            self.handler.error_message("color selection", err)

    def select_wheels_330i(self, index):
        try:

            wheels = {
                0: "//div[@data-index='0']",    # 18" v-spoke bi-color orbit grey wheels - all-season non run-flat
                1: "//div[@data-index='1']",    # 18" v-spoke bi-color orbit grey wheels - all-season run-flat
                2: "//div[@data-index='2']",    # 19" M Double-spoke bi-color jet black wheels - performance run-flat
                3: "//div[@data-index='3']",    # 19" M double-spoke bi-color jet black wheels - all-season run-flat
                4: "//div[@data-index='4']",    # 19" M double-spoke jet black wheels - high performance non run-flat
                5: "//div[@data-index='5']",    # 19" M double-spoke jet black wheels - performance run-flat
                6: "//div[@data-index='6']",    # 19" M double-spoke jet black wheels - all-season run-flat
                7: "//div[@data-index='7']"     # 19" Double-spoke bi-color orbit grey wheels - all-season run-flat
            }

            self.loadtime()
            time.sleep(2)
            wheel = self.driver.find_element_by_xpath(wheels.get(index, "invalid index"))
            self.driver.execute_script("arguments[0].scrollIntoView();", wheel)
            time.sleep(2)
            wheel.click()
            self.confirm_change()
            self.next_page()
        except Exception as err:
            self.handler.error_message("error selecting wheels", err)

    def select_upholstery_330i(self, index):
        try:

            uph_list = {
                0: "//div[@title='Canberra Beige SensaTec']",
                1: "//div[@title='Black SensaTec']",
                2: "//div[@title='Canberra Beige/Black Vernasca Leather with contrast stitching']",
                3: "//div[@title='Black Vernasca Leather with contrast stitching']",
                4: "//div[@title='Mocha Vernasca Leather with contrast stitching']",
                5: "//div[@title='Black Vernasca Leather with Black contrast stitching']",
                6: "//div[@title='Black Vernasca Leather with Blue contrast stitching']",
                7: "//div[@title='Oyster Vernasca Leather with contrast stitching']",
                8: "//div[@title='Cognac Vernasca Leather with contrast stitching']"
            }

            self.loadtime()
            time.sleep(2)
            uph = self.driver.find_element_by_xpath(uph_list.get(index, "invalid index"))
            self.driver.execute_script("arguments[0].scrollIntoView();", uph)
            time.sleep(2)
            uph.click()
            self.confirm_change()
            self.next_page()
        except Exception as err:
            self.handler.error_message("error selecting upholstery", err)

    def select_trim_330i(self, index):
        try:
            trims = {
                0: "//div[@data-index='0']",        # Open pore fine wood oak grain
                1: "//div[@data-index='1']",        # open pore fine wood maple
                2: "//div[@data-index='2']",        # fine wood - ash grey-brown high gloss
                3: "//div[@data-index='3']",        # aluminum tetragon
                4: "//div[@data-index='4']"         # aluminum - mesh effect
            }

            self.loadtime()
            time.sleep(2)
            trim = self.driver.find_element_by_xpath(trims.get(index, "invalid index"))
            self.driver.execute_script("arguments[0].scrollIntoView();", trim)
            time.sleep(2)
            trim.click()
            self.confirm_change()
            self.next_page()
        except Exception as err:
            self.handler.error_message("error selecting trim", err)

    def select_featured_package_330i(self, index):
        try:
            f_packages = {
                0: "//img[@alt='Convenience Package']",
                1: "//img[@alt='Premium Package']",
                2: "//img[@alt='Executive Package']"
            }

            self.loadtime()
            time.sleep(2)
            f_package = self.driver.find_element_by_xpath(f_packages.get(index, "invalid index"))
            time.sleep(2)
            f_package.click()
            time.sleep(2)
            addtobuild = self.driver.find_element_by_class_name(
                "package-modal__selected-btn.theme-core.byo-core-type.headline-6")
            addtobuild.click()
            self.confirm_change()
        except Exception as err:
            self.handler.error_message("error selecting featured package", err)

    def select_additional_packages_330i(self, index):
        try:
            a_packages = {
                0: "//img[@alt='Driving Assistance Package']",
                1: "//img[@alt='Driving Assistance Professional Package']",
                2: "//img[@alt='Parking Assistance Package']",
                3: "//img[@alt='Track Handling Package']"
            }

            self.loadtime()
            time.sleep(2)
            a_package = self.driver.find_element_by_xpath(a_packages.get(index, "invalid index"))
            self.driver.execute_script("arguments[0].scrollIntoView();", a_package)
            time.sleep(2)
            a_package.click()
            time.sleep(2)
            addtobuild = self.driver.find_element_by_class_name(
                "package-modal__selected-btn.theme-core.byo-core-type.headline-6")
            addtobuild.click()
            self.confirm_change()
        except Exception as err:
            self.handler.error_message("error selecting additional package", index)

    def next_page(self):
        try:
            next = self.wait.until(
                ec.element_to_be_clickable((By.CLASS_NAME, "button-next.byo-core-type.label-1.theme-core"))
            )
            next.click()
        except Exception as err:
            self.handler.error_message("error moving to next page", err)

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
            self.handler.error_message("error closing zip modal", err)
