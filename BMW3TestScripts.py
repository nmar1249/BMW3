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

    # 330i Design
    def Test_A01(self):
        try:
            print("Beginning Test Case A01")
            self.auto.select_model(0)
            self.auto.select_design_330i(1)
            self.auto.select_color_330i(7)
        except Exception as err:
            self.handler.error_message("A01", err)


'''
begin _TestScripts:

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