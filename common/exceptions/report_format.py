#------------------------------------------------
#  @brief       Classes of Exceptions for checking format of report
#  @author      Andrew Simine
#  @copyright   Copyrighted by Andrew Simine
#
#------------------------------------------------

class ReportFormatException(Exception):
    def __init__(self, message):
        self.message = message

#------------------------------------------------
