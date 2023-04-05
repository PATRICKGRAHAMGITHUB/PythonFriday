
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import platform
import getpass
from password_authentication import AuthenticatePasswordFormat
from xl_to_snowflake import xl_to_snowflake
username_attempt = 1
user_message_id = 0
password_attempts = 1


def ask_username():
    # print(f'{user_message_id} ask_username value')
    user_name_input = input(various_messages_list[user_message_id])
    check_username(user_name_input.lower())


def lower_dict(d):
    new_dict = dict((k.lower(), v.lower()) for k, v in d.items())
    return new_dict


various_messages_list = [
    'Hello, please enter your user name : ? ',
    'Please enter your user name again: ? ',
    ', please enter your Password : ? ',
    'Enter Your Password Again : ? ',
]

users_and_password_list = {
    "RajdeepB": "PasswordABC",
    "ChrisE": "Access1234",
    "SolomonP": "PassRef55",
    "AsmitaL": "Password321",
    "IanO": "Password2233",
    "PatrickG": "Access123",
    "ScottM": "PassRef22",
    "ArturH": "Password123",
}

# users_and_password_list = lower_dict(users_and_password_list)
upl = list(lower_dict(users_and_password_list).keys())


# This is an attempt to access user name as see if there is a matching value in the list
def check_username(user_name_input):
    global username_attempt
    global user_message_id

    # print(upl)
    print(user_name_input)
    if user_message_id < 1:
        user_message_id = user_message_id + 1

    if user_name_input.lower() not in upl:
        #   while user_name_input.lower() not in upl:
        print(f'{user_name_input} is not a valid user')
        if username_attempt < 3:
            username_attempt = username_attempt + 1
            ask_username()
            if username_attempt >= 2:
                print(f'You have {username_attempt} failed username attempts: ')
                print('You have one final attempt')
        else:
            print("You have exceeded the amount of permitted attempts to enter user name")
            return
    else:
        if user_name_input in upl:
            check_password(user_name_input.capitalize())
            return


def check_password(user_name_password_for_pwd):
    pwd = input(f"Hi {user_name_password_for_pwd} {various_messages_list[2]} ")

    password_correct = False

    auth_yn = AuthenticatePasswordFormat(pwd)
    print(f'{auth_yn.validate()} found validation')
    if not auth_yn.validate():
        print(auth_yn.validate())
        print("Please re-enter your password")
        check_password(user_name_password_for_pwd)

    for x, y in users_and_password_list.items():
        if user_name_password_for_pwd.capitalize() == x.capitalize() and pwd == y:
            password_correct = True
            print('** Verified, lets start to import **')
            xl_to_snowflake()
            break

    if not password_correct:
        print(f"Password: {pwd} is not correct ")
        check_password(user_name_password_for_pwd)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ask_username()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

