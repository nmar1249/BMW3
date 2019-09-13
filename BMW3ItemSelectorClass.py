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
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import  NoSuchElementException

import time
import random


class SelectItem:

    driver = webdriver
    wait = WebDriverWait
    handler = ErrorHandler
    model = ""

    changeConfirmed = False

    startingPrice = {
        0: 40750,           # 330i
        1: 42750,           # 330i xDrive
        2: 54000,           # M340i
        3: 56000            # M340i xDrive
    }

    total = int

    def __init__(self):
        self.driver = webdriver.Chrome(r"C:\drivers\chromedriver.exe")
        self.wait = WebDriverWait(self.driver, 5)
        self.handler = ErrorHandler()
        self.total = 0

    # track page loading time
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


    def select_model(self, index):
        try:
            self.driver.get("https://www.bmwusa.com/build-your-own.html#/series/3/sedan")

            models = {
                0: "//a[@title='2020 BMW 330i Sedan']",         # 330i
                1: "//a[@title='2020 BMW 330i xDrive Sedan']",  # 330i xDrive
                2: "//a[@title='2020 BMW M340i Sedan']",        # M340i
                3: "//a[@title='2020 BMW M340i xDrive Sedan']"  # M340i xDrive
            }

            self.loadtime()

            # find the button of the specified model
            button = self.wait.until(
                ec.element_to_be_clickable((By.XPATH, models.get(index, "invalid index"))))
            button.click()
            self.model = index                      # set model to index, so it can get the base price

            self.total = self.startingPrice.get(index, "invalid index")
            print("Model selected. Index: " + str(index))
            self.check_total()
        except Exception as err:
            print(str(err))
            self.replug(index)

    # are you "unplugged" from the config? replug!
    def replug(self, model):
        self.select_model(model)    # refresh model select

    # select Design - 330i
    # there is no design option for M340i
    def select_design_330i(self, index):
        try:
            self.loadtime()

            designs = {
                0: "//div[@data-index='0']",    # sport line
                1: "//div[@data-index='1']",    # luxury
                2: "//div[@data-index='2']"     # m sport
            }

            self.changeConfirmed = False
            time.sleep(2)
            design = self.driver.find_element_by_xpath(designs.get(index, "invalid index"))
            data = design.find_element_by_class_name("byo-rail-option")
            price = data.get_attribute("listprice")
            design.click()
            print("Design selected. Index: " + str(index))
            self.next_page()
            self.confirm_change()

            if self.changeConfirmed == False:
                self.total = self.total + int(price)

            self.check_total()
        except Exception as err:
            self.handler.error_message("330i - design", err)

    # select a paint job in the configurator
    def select_color(self, index):
        try:

            # 330i paint types
            colors_330i = {
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

            # m340i paint types
            colors_M340i = {
                0: "//div[@title='Alpine White']",
                1: "//div[@title='Black Sapphire Metallic']",
                2: "//div[@title='Mineral White Metallic']",
                3: "//div[@title='Mineral Grey Metallic']",
                4: "//div[@title='Sunset Orange Metallic']",
                5: "//div[@title='Portimao Blue Metallic']",
                6: "//div[@title='Dravit Gray Metallic']",
                7: "//div[@title='Tanzanite Blue II Metallic"
            }

            # resent change confirmed boolean
            self.changeConfirmed = False
            self.loadtime()

            # at this point a pop-up well appear asking to input your zip. close it
            self.close_zip()
            time.sleep(2)

            # declare price attribute
            price = 0

            # determine model
            # 330i or 330i xdrive
            if self.model == 0 or self.model == 1:

                # find color element
                color = self.driver.find_element_by_xpath(colors_330i.get(index, "invalid index"))
                self.driver.execute_script("arguments[0].scrollIntoView();", color)             # GET ELEMENT INTO VIEW

                #extract list price from element (could be 0 or 550)
                data = color.find_element_by_class_name("byo-rail-option")
                price = data.get_attribute("listprice")
                time.sleep(2)

                #click element
                color.click()

            # M340i or M340i xDrive
            elif self.model == 2 or self.model == 3:

                # find color element
                color = self.driver.find_element_by_xpath(colors_M340i.get(index, "invalid index"))
                self.driver.execute_script("arguments[0].scrollIntoView();", color)  # GET ELEMENT INTO VIEW

                # extract list price from element
                data = color.find_element_by_class_name("byo-rail-option")
                price = data.get_attribute("listprice")
                time.sleep(2)

                # click element
                color.click()

            # confirm change (if needed)
            self.confirm_change()

            # if confirm change menu didnt appear, calculate the new total
            if self.changeConfirmed == False:
                self.total = self.total + int(price)

            # verify that the total is properly displayed then move on to the next page
            self.check_total()
            self.next_page()
            print("Color selected. Index:\t" + str(index))
        except Exception as err:
            self.handler.error_message("color selection", err)

    def select_wheels(self, index):
        try:

            wheels_330i = {
                0: "//div[@data-index='0']",    # 18" v-spoke bi-color orbit grey wheels - all-season non run-flat
                1: "//div[@data-index='1']",    # 18" v-spoke bi-color orbit grey wheels - all-season run-flat
                2: "//div[@data-index='2']",    # 19" M Double-spoke bi-color jet black wheels - performance run-flat
                3: "//div[@data-index='3']",    # 19" M double-spoke bi-color jet black wheels - all-season run-flat
                4: "//div[@data-index='4']",    # 19" M double-spoke jet black wheels - high performance non run-flat
                5: "//div[@data-index='5']",    # 19" M double-spoke jet black wheels - performance run-flat
                6: "//div[@data-index='6']",    # 19" M double-spoke jet black wheels - all-season run-flat
                7: "//div[@data-index='7']"     # 19" Double-spoke bi-color orbit grey wheels - all-season run-flat
            }

            wheels_M340i = {
                0: "//div[@data-index='0']",  # 18" M Double-spoke bi-color orbit grey wheels - performance run-flat
                1: "//div[@data-index='1']",  # 18" M Double-spoke bi-color orbit grey wheels - all-season non run-flat
                2: "//div[@data-index='2']",  # 18" M Double-spoke bi-color orbit grey wheels - all-season run-flat
                3: "//div[@data-index='3']",  # 19" M Double-spoke bi-color jet black wheels - performance run-flat
                4: "//div[@data-index='4']",  # 19" M Double-spoke bi-color jet black wheels - all-season run-flat
                5: "//div[@data-index='5']",  # 19" M Double-spoke jet black wheels - high performance non run-flat
                6: "//div[@data-index='6']",  # 19" M Double-spoke jet black wheels - all-season run-flat
                7: "//div[@data-index='7']",  # 19" Double-spoke bi-color orbit grey wheels - all-season run-flat
                8: "//div[@data-index='8']",  # 19" M Double-spoke cerium grey wheels - high performance non run-flat
                9: "//div[@data-index='9']",  # 19" M Double-spoke cerium grey wheels - high performance runflat
                10: "//div[@data-index='10']" # 19" M Double-spoke cerium grey wheels - all-season run-flat
            }

            self.loadtime()
            time.sleep(2)

            # declare price variable
            price = 0

            # 330i or 330i xDrive
            if self.model == 0 or self.model == 1:

                # find element and scroll it into view
                wheel = self.driver.find_element_by_xpath(wheels_330i.get(index, "invalid index"))
                self.driver.execute_script("arguments[0].scrollIntoView();", wheel)

                # extract price attribute from the element
                data = wheel.find_element_by_class_name("byo-rail-option")
                price = data.get_attribute("listprice")
                time.sleep(2)

                # click element
                wheel.click()
            # M340i or M340i xDrive
            elif self.model == 2 or self.model == 3:
                # find element and scroll it into view
                wheel = self.driver.find_element_by_xpath(wheels_M340i.get(index, "invalid index"))
                self.driver.execute_script("arguments[0].scrollIntoView();", wheel)

                # extract price attribute and record it
                data = wheel.find_element_by_class_name("byo-rail-option")
                price = data.get_attribute("listprice")
                time.sleep(2)

                # click element
                wheel.click()

            print("selected wheel. index: " + str(index))
            self.confirm_change()

            if self.changeConfirmed == False:
                self.total = self.total + int(price)

            self.check_total()
            self.next_page()
        except Exception as err:
            self.handler.error_message("error selecting wheels", err)

    def select_upholstery(self, index):
        try:

            uph_list_330i = {
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

            uph_list_M340i = {
                1: "//div[@title='Black SensaTec']",
                2: "//div[@title='Black Vernasca Leather with contrast stitching']",
                3: "//div[@title='Mocha Vernasca Leather with contrast stitching']",
                4: "//div[@title='Black Vernasca Leather with Blue contrast stitching']",
                5: "//div[@title='Oyster Vernasca Leather with contrast stitching']",
                6: "//div[@title='Cognac Vernasca Leather with contrast stitching']"
            }

            self.changeConfirmed = False
            self.loadtime()
            time.sleep(2)

            price = 0

            # 330i or 330i xDrive
            if self.model == 0 or self.model == 1:
                # find element and scroll it into view
                uph = self.driver.find_element_by_xpath(uph_list_330i.get(index, "invalid index"))
                self.driver.execute_script("arguments[0].scrollIntoView();", uph)

                # extract listprice attribute from the element
                data = uph.find_element_by_class_name("byo-rail-option")
                price = data.get_attribute("listprice")
                time.sleep(2)

                # click element
                uph.click()

            # M340i or M340i xDrive
            elif self.model == 2 or self.model == 3:
                # find element and scroll it into view
                uph = self.driver.find_element_by_xpath(uph_list_M340i.get(index, "invalid index"))
                self.driver.execute_script("arguments[0].scrollIntoView();", uph)

                # extract listprice attribute from the element
                data = uph.find_element_by_class_name("byo-rail-option")
                price = data.get_attribute("listprice")
                time.sleep(2)

                # click element
                uph.click()

            # confirm change
            print("selected upholstery. index: " + str(index))
            self.confirm_change()

            # if no changes needed to be confirmed, calculate the price
            if self.changeConfirmed == False:
                self.total = self.total + int(price)

            # compare the backend total against the total on the UI
            self.check_total()
            self.next_page()
        except Exception as err:
            self.handler.error_message("error selecting upholstery", err)

    # same for 330i and M340i
    def select_trim(self, index):
        try:
            trims = {
                0: "//div[@data-index='0']",        # Open pore fine wood oak grain
                1: "//div[@data-index='1']",        # open pore fine wood maple
                2: "//div[@data-index='2']",        # fine wood - ash grey-brown high gloss
                3: "//div[@data-index='3']",        # aluminum tetragon
                4: "//div[@data-index='4']"         # aluminum - mesh effect
            }

            self.changeConfirmed = False
            self.loadtime()
            time.sleep(2)

            # find element and scroll it into view
            trim = self.driver.find_element_by_xpath(trims.get(index, "invalid index"))
            self.driver.execute_script("arguments[0].scrollIntoView();", trim)

            # extract listprice attribute from the element
            data = trim.find_element_by_class_name("byo-rail-option")
            price = data.get_attribute("listprice")
            time.sleep(2)

            # click element
            trim.click()
            print("selected trim. index: " + str(index))

            # confirm change
            self.confirm_change()

            # if change isnt confirmed calculate the total
            if self.changeConfirmed == False:
                self.total = self.total + int(price)

            # compare backend total against the total on UI then proceed
            self.check_total()
            self.next_page()
        except Exception as err:
            self.handler.error_message("error selecting trim", err)

    def select_featured_package(self, index):
        try:
            f_packages_330i = {
                0: "//img[@alt='Convenience Package']",
                1: "//img[@alt='Premium Package']",
                2: "//img[@alt='Executive Package']"
            }

            f_packages_M340i = {
                0: "//img[@alt='Premium Package']",
                1: "//img[@alt='Executive Package']"
            }

            self.changeConfirmed = False
            self.loadtime()
            time.sleep(2)

            # 330i or 330i xDrive
            if self.model == 0 or self.model == 1:
                # find element and click
                f_package = self.driver.find_element_by_xpath(f_packages_330i.get(index, "invalid index"))
                time.sleep(2)
                f_package.click()
            # M340i or M340i xDrive
            elif self.model == 2 or self.model == 3:
                # find element and click
                f_package = self.driver.find_element_by_xpath(f_packages_M340i.get(index, "invalid index"))
                time.sleep(2)
                f_package.click()

            # extract listprice attribute
            price = self.driver.find_element_by_class_name("package-modal__price.theme-core.byo-core-type.headline-6")
            time.sleep(2)

            # click the add to build button
            addtobuild = self.driver.find_element_by_class_name(
                "package-modal__selected-btn.theme-core.byo-core-type.headline-6")
            addtobuild.click()
            print("selected featured package. index: " + str(index))
            self.confirm_change()

            # calculate the price if there were no changes to confirm
            if self.changeConfirmed == False:
                self.total = self.total + int(''.join(c for c in price.text if c.isdigit()))

            # compare the backend total to the total on the UI
            self.check_total()
        except Exception as err:
            self.handler.error_message("error selecting featured package", err)

    def select_additional_packages(self, index):
        try:
            a_packages_330i = {
                0: "//button[contains(text(), 'Driving Assistance Package')]",
                1: "//button[contains(text(), 'Driving Assistance Professional Package')]",
                2: "//button[contains(text(), 'Parking Assistance Package')]",
                3: "//button[contains(text(), 'Track Handling Package')]"
            }

            a_packages_M340i = {
                0: "//button[contains(text(), 'Driving Assistance Package')]",
                1: "//button[contains(text(), 'Driving Assistance Professional Package')]",
                2: "//button[contains(text(), 'Parking Assistance Package')]",
                3: "//button[contains(text(), 'Cooling and High Performance Tire Package')]"
            }

            # reset confirmed change boolean
            self.changeConfirmed = False
            self.loadtime()
            time.sleep(2)

            # 330i or 330i xDrive
            if self.model == 0 or self.model == 1:
                a_package = self.driver.find_element_by_xpath(a_packages_330i.get(index, "invalid index"))
                self.driver.execute_script("arguments[0].scrollIntoView();", a_package)
                time.sleep(2)
                action(self.driver).send_keys(Keys.UP).send_keys(Keys.UP).send_keys(Keys.UP).perform() # bring the element into view
                time.sleep(3)
                a_package.click()

            # M340i or M340i xDrive
            elif self.model == 2 or self.model == 3:
                a_package = self.driver.find_element_by_xpath(a_packages_M340i.get(index, "invalid index"))
                self.driver.execute_script("arguments[0].scrollIntoView();", a_package)
                time.sleep(2)
                action(self.driver).send_keys(Keys.UP).send_keys(Keys.UP).send_keys(
                    Keys.UP).perform()  # bring the element into view
                time.sleep(3)
                a_package.click()

            # extract price attribute
            price = self.driver.find_element_by_class_name(
                "package-modal__price.package-modal__price--add-pkg.theme-core.byo-core-type.headline-6")

            # click add to build
            addtobuild = self.driver.find_element_by_class_name(
                "package-modal__selected-btn.theme-core.byo-core-type.headline-6")
            addtobuild.click()
            time.sleep(6)
            print("Selected additional package. Index: " + str(index))
            self.confirm_change()

            # run calculations of no changes were confirmed
            if self.changeConfirmed == False:
                self.total = self.total + int(''.join(c for c in price.text if c.isdigit()))

            self.check_total()
        except Exception as err:
            self.handler.error_message("error selecting additional package", err)

    # add is a boolean variable that determines whether an item is being added (true) or removed (false)
    def select_all_options(self, index, add):
        try:
            options_330i = {
                0: "//button[contains(text(), 'Space-saver spare')]",
                1: "//button[contains(text(), 'Park Distance Control')]",
                2: "//button[contains(text(), 'Remote Engine Start')]",
                3: "//button[contains(text(), 'Heated Steering Wheel')]",
                4: "//button[contains(text(), 'Power tailgate')]",
                5: "//button[contains(text(), 'Heated front seats')]",
                6: "//button[contains(text(), 'SensaTec Dashboard')]",
                7: "//button[contains(text(), 'Ambient Lighting')]",
                8: "//button[contains(text(), 'Wireless Charging and WiFi Hotspot')]",
                9: "//button[contains(text(), 'Live Cockpit Pro (incl. Navi)')]",
                10: "//button[contains(text(), 'Harman Kardon surround sound system')]",
                11: "//button[contains(text(), 'Adaptive M Suspension')]"
            }

            options_M340i = {
                0: "//button[contains(text(), 'Space-saver spare')]",
                1: "//button[contains(text(), 'Park Distance Control')]",
                2: "//button[contains(text(), 'Active Cruise Control')]",
                3: "//button[contains(text(), 'Remote Engine Start')]",
                4: "//button[contains(text(), 'Heated Steering Wheel')]",
                5: "//button[contains(text(), 'Power tailgate')]",
                6: "//button[contains(text(), 'Heated front seats')]",
                7: "//button[contains(text(), 'Ambient Lighting')]",
                8: "//button[contains(text(), 'Wireless Charging and WiFi Hotspot')]",
                9: "//button[contains(text(), 'Harman Kardon surround sound system')]",
                10: "//button[contains(text(), 'Adaptive M Suspension')]"
            }

            self.loadtime()

            time.sleep(3)

            # 330i or 330i xDrive
            if self.model == 0 or self.model == 1:
                option = self.wait.until(ec.element_to_be_clickable((By.XPATH, options_330i.get(index, "invalid index"))))
                self.driver.execute_script("arguments[0].scrollIntoView();", option)
                action(self.driver).send_keys(Keys.UP).send_keys(Keys.UP).send_keys(
                    Keys.UP).perform()  # bring the element into view
                time.sleep(2)
                option.click()

            # M#40i or M340i xDrive
            elif self.model == 2 or self.model == 3:
                option = self.wait.until(
                    ec.element_to_be_clickable((By.XPATH, options_M340i.get(index, "invalid index"))))
                self.driver.execute_script("arguments[0].scrollIntoView();", option)
                action(self.driver).send_keys(Keys.UP).send_keys(Keys.UP).send_keys(
                    Keys.UP).perform()  # bring the element into view
                time.sleep(2)
                option.click()

            # if item is being added
            if add == True:
                price = self.driver.find_element_by_class_name(
                    "detail-modal-price.theme-core.byo-core-type.headline-5")
                addtobuild = self.wait.until(ec.element_to_be_clickable(
                    (By.CLASS_NAME, "detail-modal-button-add-item.cta-1" )
                ))
                addtobuild.click()
            # else its being removed
            else:
                price = self.driver.find_element_by_class_name(
                    "detail-modal-price.theme-core.byo-core-type.headline-5")
                remove = self.wait.until(ec.element_to_be_clickable(
                    (By.CLASS_NAME, "detail-modal-button-addi-item.active.cta-1")
                ))
                remove.click()

            # close window
            time.sleep(2)
            close = self.wait.until(ec.element_to_be_clickable((By.CLASS_NAME, "close-button")))
            close.click()
            print("Selected options. index: " + str(index))
            self.confirm_change()

            # if no changes are confirmed, calculate the price based on the add boolean
            if self.changeConfirmed == False:
                if add == True:
                    self.total = self.total + int(''.join(c for c in price.text if c.isdigit()))
                elif add == False:
                    self.total = self.total - int(''.join(c for c in price.text if c.isdigit()))

            self.check_total()
            self.next_page_dock()

        except Exception as err:
            self.select_all_options(index, False) # perhaps it needs to be removed, try that.
            self.handler.error_message("error selecting options", err)

    # choose accessories for the vehicle configurator
    def select_accessories(self, index, add):
        try:
            accessories_330i = {
                0: "//button[contains(text(), 'BMW Protective Rear Cover')]"
            }

            accessories_M340i = {
                0: "//button[contains(text(), 'BMW Protective Rear Cover')]",
                1: "//button[contains(text(), 'BMW Loading Sill Mat')]"
            }

            self.loadtime()

            # 330i or 330i xDrive
            if self.model == 0 or self.model == 1:
                accessory = self.wait.until(ec.element_to_be_clickable((By.XPATH, accessories_330i.get(index, "invalid index"))))
                time.sleep(4)
                accessory.click()
            # M340i or M340i xDrive
            elif self.model == 2 or self.model == 3:
                accessory = self.wait.until(ec.element_to_be_clickable((By.XPATH, accessories_M340i.get(index, "invalid index"))))
                time.sleep(4)
                accessory.click()

            # if item is to be added
            if add == True:
                addtobuild = self.wait.until(ec.element_to_be_clickable(
                    (By.CLASS_NAME, "detail-modal-button-add-item.cta-1")
                ))
                addtobuild.click()
            # if item is to be removed
            else:
                remove = self.wait.until(ec.element_to_be_clickable(
                    (By.CLASS_NAME, "detail-modal-button-addi-item.active.cta-1")   # xpath for removal button
                ))
                remove.click()

            time.sleep(2)
            close = self.wait.until(ec.element_to_be_clickable((By.CLASS_NAME, "close-button")))
            close.click()
            print("Selected accessory index: " + str(index))
            self.confirm_change()
            self.check_total()
            self.next_page_dock()

        except Exception as err:
            self.handler.error_message("error selecting accessories", err)

    # go to the next page in the configurator
    def next_page(self):
        try:
            next = self.wait.until(
                ec.element_to_be_clickable((By.CLASS_NAME, "button-next.byo-core-type.label-1.theme-core"))
            )
            next.click()
        except Exception as err:
            self.handler.error_message("error moving to next page", err)

    # go to the final page (different xpath than previous method
    def next_page_dock(self):
        try:
            next = self.wait.until(
                ec.element_to_be_clickable((By.CLASS_NAME, "byo-core-type.byo-dock__link.theme-gkl.label-1"))
            )
            next.click()
        except Exception as err:
            self.handler.error_message("error moving to next page", err)

    # confirm change
    # this method handles the pop-up menu that asks a user to confirm changes when an item
    # is exclusive to another item. The price calculation is not always accurate since not all
    # items are shown on the screen.
    def confirm_change(self):
        try:
            time.sleep(2)
            #get the net value of the change
            nc_element = self.driver.find_element_by_class_name("conflict-modal__value.byo-core-type.theme-gkl.label-1")
            netChange = nc_element.text

            print("Net Change:\t" + str(netChange))

            # if change is positive, add to total, if it is negative, subtract
            if netChange[0] == '+':
                self.total = self.total + int(''.join(c for c in netChange if c.isdigit())) # this line removes all
                                                                                            # non digits from the
                                                                                            # string.
            elif netChange[0] == '-':
                self.total = self.total - int(''.join(c for c in netChange if c.isdigit()))

            # click confirm
            confirm = self.wait.until(ec.element_to_be_clickable((By.XPATH, "//button[@name='confirm-button']")))
            confirm.click()
            print("change confirmed! current total:\t" + str(self.total))
            self.changeConfirmed = True # change has been confirmed, ignore end calculations
        except NoSuchElementException:
            print("No changes to confirm.")
        except Exception as err:
            self.handler.error_message("Error confirming change!", err)

    # closes zipcode window - can cause click intercepts if open
    def close_zip(self):
        try:
            time.sleep(4) # wait for the banner to disappear
            # close zip pop-up
            close = self.wait.until(ec.element_to_be_clickable((By.XPATH, "//button[@aria-label='Close Zipcode Modal']")))
            close.click()
        except Exception as err:
            self.handler.error_message("error closing zip modal", err)

    # calculate the listprice attribute and compare it to the total displayed on the UI
    def check_total(self):
        try:
            # show total calculated on backend
            print("Backend total: " + str(self.total))

            # get the total displayed on the UI
            display = self.driver.find_element_by_class_name(
                "total-amount.core-type.theme-core.total-amount--bold.headline-5")

            displayTotal = int(''.join(c for c in display.text if c.isdigit())) # remove non-digits

            # print total on UI
            print("Total on UI: " + str(displayTotal))

            # verify that the totals are equal
            if self.total != displayTotal:
                # if they arent, send a message
                print("Total on UI does not match!")
                print("Difference (total - displayTotal): " + str(self.total - displayTotal) )
            else:
                print("Totals match!")  # they match, woo
        except Exception as err:
            self.handler.error_message("error checking total", err)