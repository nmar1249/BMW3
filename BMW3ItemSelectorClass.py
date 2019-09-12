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

import time

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

            button = self.wait.until(
                ec.element_to_be_clickable((By.XPATH, models.get(index, "invalid index"))))
            button.click()
            self.model = index

            self.total = self.startingPrice.get(index, "invalid index")
            print("Model selected. Index: " + str(index))
            self.check_total()
        except Exception as err:
            print(str(err))
            self.replug(index)

    # are you "unplugged" from the config? replug!
    def replug(self, model):
        self.select_model(model)

    # select Design - 330i
    # there is no design option for M340i
    def select_design_330i(self, index):
        try:
            self.loadtime()

            designs = {
                0: "//div[@data-index='0']",
                1: "//div[@data-index='1']",
                2: "//div[@data-index='2']"
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

    def select_color(self, index):
        try:

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

            self.changeConfirmed = False
            self.loadtime()
            self.close_zip()
            time.sleep(2)

            price = 0
            # determine model
            if self.model == 0 or self.model == 1:
                color = self.driver.find_element_by_xpath(colors_330i.get(index, "invalid index"))
                self.driver.execute_script("arguments[0].scrollIntoView();", color)             # GET ELEMENT INTO VIEW
                data = color.find_element_by_class_name("byo-rail-option")
                price = data.get_attribute("listprice")
                time.sleep(2)
                color.click()
            elif self.model == 2 or self.model == 3:
                color = self.driver.find_element_by_xpath(colors_M340i.get(index, "invalid index"))
                self.driver.execute_script("arguments[0].scrollIntoView();", color)  # GET ELEMENT INTO VIEW
                data = color.find_element_by_class_name("byo-rail-option")
                price = data.get_attribute("listprice")
                time.sleep(2)
                color.click()

            self.confirm_change()
            if self.changeConfirmed == False:
                self.total = self.total + int(price)


            self.check_total()
            self.next_page()
            print("Color selected. Index: " + str(index))
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
                                            #TODO change these comments to reflect the M340i wheel selection
            wheels_M340i = {
                0: "//div[@data-index='0']",  # 18" v-spoke bi-color orbit grey wheels - all-season non run-flat
                1: "//div[@data-index='1']",  # 18" v-spoke bi-color orbit grey wheels - all-season run-flat
                2: "//div[@data-index='2']",  # 19" M Double-spoke bi-color jet black wheels - performance run-flat
                3: "//div[@data-index='3']",  # 19" M double-spoke bi-color jet black wheels - all-season run-flat
                4: "//div[@data-index='4']",  # 19" M double-spoke jet black wheels - high performance non run-flat
                5: "//div[@data-index='5']",  # 19" M double-spoke jet black wheels - performance run-flat
                6: "//div[@data-index='6']",  # 19" M double-spoke jet black wheels - all-season run-flat
                7: "//div[@data-index='7']",  # 19" Double-spoke bi-color orbit grey wheels - all-season run-flat
                8: "//div[@data-index='8']",  # 19" Double-spoke bi-color orbit grey wheels - all-season run-flat
                9: "//div[@data-index='9']",  # 19" Double-spoke bi-color orbit grey wheels - all-season run-flat
                10: "//div[@data-index='10']"
            }

            self.loadtime()
            time.sleep(2)

            price = 0
            if self.model == 0 or self.model == 1:
                wheel = self.driver.find_element_by_xpath(wheels_330i.get(index, "invalid index"))
                self.driver.execute_script("arguments[0].scrollIntoView();", wheel)
                data = wheel.find_element_by_class_name("byo-rail-option")
                price = data.get_attribute("listprice")
                time.sleep(2)
                wheel.click()
            elif self.model == 2 or self.model == 3:
                wheel = self.driver.find_element_by_xpath(wheels_M340i.get(index, "invalid index"))
                self.driver.execute_script("arguments[0].scrollIntoView();", wheel)
                data = wheel.find_element_by_class_name("byo-rail-option")
                price = data.get_attribute("listprice")
                time.sleep(2)
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
            if self.model == 0 or self.model == 1:
                uph = self.driver.find_element_by_xpath(uph_list_330i.get(index, "invalid index"))
                self.driver.execute_script("arguments[0].scrollIntoView();", uph)
                data = uph.find_element_by_class_name("byo-rail-option")
                price = data.get_attribute("listprice")
                time.sleep(2)
                uph.click()
            elif self.model == 2 or self.model == 3:
                uph = self.driver.find_element_by_xpath(uph_list_M340i.get(index, "invalid index"))
                self.driver.execute_script("arguments[0].scrollIntoView();", uph)
                data = uph.find_element_by_class_name("byo-rail-option")
                price = data.get_attribute("listprice")
                time.sleep(2)
                uph.click()

            print("selected upholstery. index: " + str(index))
            self.confirm_change()

            if self.changeConfirmed == False:
                self.total = self.total + int(price)

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
            trim = self.driver.find_element_by_xpath(trims.get(index, "invalid index"))
            self.driver.execute_script("arguments[0].scrollIntoView();", trim)
            data = trim.find_element_by_class_name("byo-rail-option")
            price = data.get_attribute("listprice")
            time.sleep(2)
            trim.click()
            print("selected trim. index: " + str(index))
            self.confirm_change()

            if self.changeConfirmed == False:
                self.total = self.total + int(price)

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
            if self.model == 0 or self.model == 1:
                f_package = self.driver.find_element_by_xpath(f_packages_330i.get(index, "invalid index"))
                time.sleep(2)
                f_package.click()
            elif self.model == 2 or self.model == 3:
                f_package = self.driver.find_element_by_xpath(f_packages_M340i.get(index, "invalid index"))
                time.sleep(2)
                f_package.click()

            price = self.driver.find_element_by_class_name("package-modal__price.theme-core.byo-core-type.headline-6")
            time.sleep(2)
            addtobuild = self.driver.find_element_by_class_name(
                "package-modal__selected-btn.theme-core.byo-core-type.headline-6")
            addtobuild.click()
            print("selected featured package. index: " + str(index))
            self.confirm_change()

            if self.changeConfirmed == False:
                self.total = self.total + int(''.join(c for c in price.text if c.isdigit()))

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

            self.changeConfirmed = False
            self.loadtime()
            time.sleep(2)
            if self.model == 0 or self.model == 1:
                a_package = self.driver.find_element_by_xpath(a_packages_330i.get(index, "invalid index"))
                self.driver.execute_script("arguments[0].scrollIntoView();", a_package)
                time.sleep(2)
                action(self.driver).send_keys(Keys.UP).send_keys(Keys.UP).send_keys(Keys.UP).perform() # bring the element into view
                time.sleep(3)
                a_package.click()
            elif self.model == 2 or self.model == 3:
                a_package = self.driver.find_element_by_xpath(a_packages_M340i.get(index, "invalid index"))
                self.driver.execute_script("arguments[0].scrollIntoView();", a_package)
                time.sleep(2)
                action(self.driver).send_keys(Keys.UP).send_keys(Keys.UP).send_keys(
                    Keys.UP).perform()  # bring the element into view
                time.sleep(3)
                a_package.click()

            price = self.driver.find_element_by_class_name(
                "package-modal__price.package-modal__price--add-pkg.theme-core.byo-core-type.headline-6")
            addtobuild = self.driver.find_element_by_class_name(
                "package-modal__selected-btn.theme-core.byo-core-type.headline-6")
            addtobuild.click()
            time.sleep(6)
            print("Selected additional package. Index: " + str(index))
            self.confirm_change()

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

            if self.model == 0 or self.model == 1:
                option = self.wait.until(ec.element_to_be_clickable((By.XPATH, options_330i.get(index, "invalid index"))))
                self.driver.execute_script("arguments[0].scrollIntoView();", option)
                action(self.driver).send_keys(Keys.UP).send_keys(Keys.UP).send_keys(
                    Keys.UP).perform()  # bring the element into view
                time.sleep(2)
                option.click()
            elif self.model == 2 or self.model == 3:
                option = self.wait.until(
                    ec.element_to_be_clickable((By.XPATH, options_M340i.get(index, "invalid index"))))
                self.driver.execute_script("arguments[0].scrollIntoView();", option)
                action(self.driver).send_keys(Keys.UP).send_keys(Keys.UP).send_keys(
                    Keys.UP).perform()  # bring the element into view
                time.sleep(2)
                option.click()

            if add == True:
                price = self.driver.find_element_by_class_name(
                    "detail-modal-price.theme-core.byo-core-type.headline-5")
                addtobuild = self.wait.until(ec.element_to_be_clickable(
                    (By.CLASS_NAME, "detail-modal-button-add-item.cta-1" )
                ))
                addtobuild.click()
            else:
                price = self.driver.find_element_by_class_name(
                    "detail-modal-price.theme-core.byo-core-type.headline-5")
                remove = self.wait.until(ec.element_to_be_clickable(
                    (By.CLASS_NAME, "detail-modal-button-addi-item.active.cta-1")
                ))
                remove.click()

            time.sleep(2)
            close = self.wait.until(ec.element_to_be_clickable((By.CLASS_NAME, "close-button")))
            close.click()
            print("Selected options. index: " + str(index))
            self.confirm_change()

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

            if self.model == 0 or self.model == 1:
                accessory = self.wait.until(ec.element_to_be_clickable((By.XPATH, accessories_330i.get(index, "invalid index"))))
                time.sleep(2)
                accessory.click()
            elif self.model == 2 or self.model == 3:
                accessory = self.wait.until(ec.element_to_be_clickable((By.XPATH, accessories_M340i.get(index, "invalid index"))))
                time.sleep(2)
                accessory.click()

            if add == True:
                addtobuild = self.wait.until(ec.element_to_be_clickable(
                    (By.CLASS_NAME, "detail-modal-button-add-item.cta-1")
                ))
                addtobuild.click()
            else:
                remove = self.wait.until(ec.element_to_be_clickable(
                    (By.CLASS_NAME, "detail-modal-button-addi-item.active.cta-1")
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


    def next_page(self):
        try:
            next = self.wait.until(
                ec.element_to_be_clickable((By.CLASS_NAME, "button-next.byo-core-type.label-1.theme-core"))
            )
            next.click()
        except Exception as err:
            self.handler.error_message("error moving to next page", err)

    def next_page_dock(self):
        try:
            next = self.wait.until(
                ec.element_to_be_clickable((By.CLASS_NAME, "byo-core-type.byo-dock__link.theme-gkl.label-1"))
            )
            next.click()
        except Exception as err:
            self.handler.error_message("error moving to next page", err)
    def confirm_change(self):
        try:
            time.sleep(2)
            nc_element = self.driver.find_element_by_class_name("conflict-modal__value.byo-core-type.theme-gkl.label-1")
            netChange = nc_element.text

            print("Net Change: " + str(netChange))
            if netChange[0] == '+':
                self.total = self.total + int(''.join(c for c in netChange if c.isdigit())) # get a raw int version of the price
            elif netChange[0] == '-':
                self.total = self.total - int(''.join(c for c in netChange if c.isdigit()))

            confirm = self.wait.until(ec.element_to_be_clickable((By.XPATH, "//button[@name='confirm-button']")))
            confirm.click()
            print("change confirmed! current total: " + str(self.total))
            self.changeConfirmed = True # change has been confirmed, ignore end calculations
        except Exception as err:
            self.handler.error_message("no changes to confirm", err)

    # closes zipcode window - can cause click intercepts if open
    def close_zip(self):
        try:
            time.sleep(4) # wait for the banner to disappear
            close = self.wait.until(ec.element_to_be_clickable((By.XPATH, "//button[@aria-label='Close Zipcode Modal']")))
            close.click()
        except Exception as err:
            self.handler.error_message("error closing zip modal", err)

    def check_total(self):
        try:
            print("Current total: " + str(self.total))

            display = self.driver.find_element_by_class_name(
                "total-amount.core-type.theme-core.total-amount--bold.headline-5")

            displayTotal = int(''.join(c for c in display.text if c.isdigit()))

            print("Total on UI: " + str(displayTotal))

            if self.total != displayTotal:
                print("Total on UI does not match!")
                print("Difference (total - displayTotal): " + str(self.total - displayTotal) )
            else:
                print("Totals match!")
        except Exception as err:
            self.handler.error_message("error checking total", err)