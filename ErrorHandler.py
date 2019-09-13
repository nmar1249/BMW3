import sys

class ErrorHandler:

    def error_message(self, module, err):
        print("ID:\t\t" + module)
        print("Exception thrown: " + str(err))