import sys

class ErrorHandler:

    def error_message(self, module, err):
        print("Exception thrown: " + str(err))
        print("ID:\t\t" + module)