'''
(PROJECTNAME)TestScripts
This is a template class for building test script preconditions using functionality
from the ItemSelectorClass and TestScripts.
This class will act as a "sandbox" where functionality from TestScripts can be tested. This class only uses
one test case out of each category in order to reach a point in flow where a module can be tested. The one test
case used should be the least likely to fail.
note: try/except is redundant since we are calling functions that have it implemented already.
'''

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains as action
from selenium.webdriver.support.ui import Select
from BMW3TestScripts import TestScripts # import test scripts
import time
import random


class preconditions:

    scripts = TestScripts()

    def sandbox(self):
        self.scripts.Test_A01()


# sandbox testing
test = preconditions
test.scripts.Test_B01()

'''
begin _TestScripts:
    define class variables
    (it should just be TestScripts defined as scripts)
    define initialization(self):
        create a TestScripts object called scripts
    define precondition_A():
        call a test case from A that will likely pass

    define precondition_B():
        call a test case from B that will likely pass

    define precondition_C():
        call a test case from C that will likely pass

    define preconditiojn_D():
        call a test case from D that will likely pass

    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^       
    CONTINUE DOING THIS FOR EVERY SINGLE TEST CASE!!!        

    define sandbox():
        this is where you will be testing code from TestScripts using preconditions.
        e.x. you want to test code for TestCase E05

        precondition_A()
        precondition_B()
        precondition_C()
        precondition_D()
        TestScripts.Test_E05()  # method we are testing, calling preconditions to get to this point


'''