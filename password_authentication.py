#!/usr/bin/env python3

class AuthenticatePasswordFormat():
    def __init__(self, username = ''):
        self.username = username

    def __lower(self):
        lower = any(c.islower() for c in self.username)
        return lower

    def __upper(self):
        upper = any(c.isupper() for c in self.username)
        return upper

    def __digit(self):
        """
        Return ADO environments for a specified project name

        :param connection: Connection to the ADO organization
        :type connection: Connection
        :param project_name: The ADO project name
        :type project_name: str
        :return: List of environments for specified project
        :rtype: List
        """
        digit = any(c.isdigit() for c in self.username)
        return digit


    def validate(self):
        """
        Return ADO environments for a specified project name

        :param connection: Connection to the ADO organization
        :type connection: Connection
        :param project_name: The ADO project name
        :type project_name: str
        :return: List of environments for specified project
        :rtype: List
        """
        lower = self.__lower()
        upper = self.__upper()
        digit = self.__digit()

        length = len(self.username)

        report = lower and upper and digit and length >= 6

        if report:
            print("Password has passed all checks")
            return True

        elif not lower:
            print("You didn't use any lower case letter in your password")
            return False

        elif not upper:
            print("You didn't use any Upper case letters in your password")
            return False

        elif length < 6:
            print("Password should have at least 6 character in your password")
            return False

        elif not digit:
            print("You didn't use a digit in the password")
            return False
        else:
            pass
