'''
(PROJECTNAME)TestScripts
This is a template class for building test scripts using functionality
from the ItemSelectorClass
'''


from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains as action
from selenium.webdriver.support.ui import Select
from BMW3ItemSelectorClass import SelectItem  # import functionality
from ErrorHandler import ErrorHandler

import time
import random


class TestScripts:

    handler = ErrorHandler()
    auto = SelectItem()

    # 330i sandbox flow
    def Test_A01(self):
        try:
            print("Beginning Test Case A01")
            self.auto.select_model(1)
            self.auto.select_design_330i(1)
            self.auto.select_color(7)
            self.auto.select_wheels(2)
            self.auto.select_upholstery_330i(7)
            self.auto.select_trim_330i(3)
            self.auto.select_featured_package_330i(1)
            self.auto.select_additional_packages_330i(0)
            self.auto.select_all_options_330i(7, True)
            self.auto.select_accessories_330i(0, True)
        except Exception as err:
            self.handler.error_message("A01", err)

    # M340i sandbox flow
    def Test_B01(self):
        try:
            print("Beginning Test Case B01")
            self.auto.select_model(2)
            self.auto.select_color(4)
            self.auto.select_wheels(9)
        except Exception as err:
            self.handler.error_message("B01", err)

'''

    define class variables
    (it should just be TestModule defined as ItemSelectorClass)

    define initialization(self):
        create a ItemSelectorClass object called TestModule

    define Test_A0():
        try:
            using methods from the ItemSelectorClass, program the steps for Test_A0
            print success message
        except:
            print failure/error message

    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^       
    CONTINUE DOING THIS FOR EVERY SINGLE TEST CASE!!!        
'''