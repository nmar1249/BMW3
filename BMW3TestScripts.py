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

    handler = ErrorHandler()    # error handler class
    auto = SelectItem()         # item selector object

    # A01 - Adding designs to the 330i sedan
    def Test_A01(self):
        try:
            # 0 - 330i, 1 - 330i xDrive
            print("Beginning Test Case A01")
            self.auto.select_model(random.randint(0, 1))           # 330i or 330i xDrive
            self.auto.select_design_330i(random.randint(0, 2))     # design is only available for 330i(xDrive) models
            print("Test A01 has finished executing with no issues.")
        except Exception as err:
            self.handler.error_message("A01", err)

    # A02 - Adding exterior options to the 330i sedan
    def Test_A02(self):
        try:
            # 0 - 330i, 1 - 330i xDrive, 2 - M340i, 3 - M340i xDrive
            self.Test_A01()

            print("Beginning Test Case A02")
            self.auto.select_color(random.randint(0, 11)) # randomize paint color
            self.auto.select_wheels(random.randint(0, 7)) # randomize wheel type
            print("Test A02 has finished executing with no issues.")
        except Exception as err:
            self.handler.error_message("A02", err)


    # A03 - Adding interior options to the 330i sedan
    def Test_A03(self):
        try:
            # 0 - 330i, 1 - 330i xDrive, 2 - M340i, 3 - M340i xDrive
            self.Test_A02()

            print("Beginning Test Case A03")
            self.auto.select_upholstery(random.randint(0, 8)) # select random upholstery style
            self.auto.select_trim(random.randint(0, 4))       # select random trim style
            print("Test A03 has finished executing with no issues.")
        except Exception as err:
            self.handler.error_message("A03", err)

    # A04 - Adding packages to the 330i sedan
    def Test_A04(self):
        try:
            self.Test_A03()

            print("Beginning Test Case A04")
            self.auto.select_featured_package(random.randint(0, 2))
            self.auto.select_additional_packages(random.randint(0, 3))
            print("Test A04 has finished executing with no issues.")
        except Exception as err:
            self.handler.error_message("A04", err)

    # A05/A06 - Adding "all options" to the 330i sedan and accessory (there is only one for 330i)
    def Test_A05n6(self):
        try:
            self.Test_A04()

            print("Beginning Test Case A05n6")
            self.auto.select_all_options(random.randint(0, 11), True)  # true = adding item, false = removing item
            self.auto.select_accessories(0, True)                      # isnt always available
            print("Test A05n6 has finished executing with no issues.")
        except Exception as err:
            self.handler.error_message("A05n6", err)


    # BEGIN M340i TEST CASES

    # B01 - Adding exterior options to the M340i sedan
    # model is selected here too since there is no design option for M variants
    def Test_B01(self):
        try:
            # 0 - 330i, 1 - 330i xDrive, 2 - M340i, 3 - M340i xDrive

            print("Beginning Test Case B01")
            self.auto.select_model(random.randint(2, 3))  # M340i or M340i xDrive
            self.auto.select_color(random.randint(0, 7)) # randomize paint color
            self.auto.select_wheels(random.randint(0, 10)) # randomize wheel type
            print("Test B01 has finished executing with no issues.")
        except Exception as err:
            self.handler.error_message("B01", err)


    # B02 - Adding interior options to the M340i sedan
    def Test_B02(self):
        try:
            # 0 - 330i, 1 - 330i xDrive, 2 - M340i, 3 - M340i xDrive
            self.Test_B01()

            print("Beginning Test Case B02")
            self.auto.select_upholstery(random.randint(0, 5)) # select random upholstery style
            self.auto.select_trim(random.randint(0, 4))       # select random trim style
            print("Test B02 has finished executing with no issues.")
        except Exception as err:
            self.handler.error_message("B02", err)

    # B03 - Adding packages to the M340i sedan
    def Test_B03(self):
        try:
            self.Test_B02()

            print("Beginning Test Case B03")
            self.auto.select_featured_package(random.randint(0, 1))
            self.auto.select_additional_packages(random.randint(0, 3))
            print("Test B03 has finished executing with no issues.")
        except Exception as err:
            self.handler.error_message("B03", err)

    # B04 - Adding "all options" to the M340i sedan
    def Test_B04(self):
        try:
            self.Test_B03()

            print("Beginning Test Case B04")
            self.auto.select_all_options(random.randint(0, 10), True)  # true = adding item, false = removing item
            print("Test B04 has finished executing with no issues.")
        except Exception as err:
            self.handler.error_message("B04", err)

    # B05 - adding vehicle maintenace program to M340i build
    def Test_B05(self):
        try:
            self.Test_B04()

            print("Beginning Test Case B05")
            self.auto.select_maintenance_program(random.randint(0, 4), True)
            print("Test B05 has finished executing with no issues.")
        except Exception as err:
            self.handler.error_message("B05", err)

    # B05 - adding accessories to M340i build
    def Test_B06(self):
        try:
            self.Test_B05()

            print("Beginning Test Case B06")
            self.auto.select_accessories(random.randint(0, 1), True)
            print("Test B05 has finished executing with no issues.")
        except Exception as err:
            self.handler.error_message("B06", err)
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