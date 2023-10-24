from typing import Tuple, List

from base import AddressBook, Record

records = dict()
contacts = AddressBook()


def input_error(func: callable) -> callable:
    """
    Decorator that wraps the function to handle possible errors.
    :param func: Function that should be wrapped.
    :return: Wrapped function.
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as err:
            print(f"There is no such key {err}. Type a correct name!")
        except ValueError as err:
            print(f"Passed values are incorrect. The trace error is '{err}'")
        except IndexError as err:
            print(f"Not all parameters have been passed. Check it, please.")

    return wrapper


@input_error
def parse_cli_command(cli_input: str) -> Tuple[str, callable, List[str]]:
    """
    Method that parses the typed commands from CLI.
    :param cli_input: String from CLI.
    :return: Function name, function object and function arguments.
    """
    if cli_input == ".":
        return "good_bye", COMMANDS["good bye"], []
    for command_name, func in COMMANDS.items():
        if cli_input.lower().startswith(command_name):
            return command_name, func, cli_input[len(command_name):].strip().split()
    return "unknown", unknown, []


@input_error
def hello() -> str:
    """
    Method that returns greeting to the user.
    :return: Greeting string.
    """
    return "How can I help you?"


@input_error
def add_contact(*args) -> str:
    """
    Method that adds user contacts to the AddressBook.
    :param args: Username and phone that should be stored.
    :return: Successful string about adding contact.
    """
    name = args[0]
    phone = args[1]
    birthday = None
    if len(args) > 2:
        birthday = args[2]
    rec = contacts.find(name)
    if rec:
        found_phone, _ = rec.get_phone_by_number(phone_num=phone)
        if not found_phone:
            add_birthday_str = rec.add_birthday(birthday=birthday)
            add_phone_str = rec.add_phone(phone)
            return f"'{add_birthday_str}', '{add_phone_str}'"
    rec = Record(name=name, birthday=birthday)
    rec.add_phone(phone_num=phone)
    contacts.add_record(rec)
    return f"The contact with name '{name}', '{phone}' and '{birthday}' has been " \
           f"successfully added"


@input_error
def change_phone(*args) -> None:
    """
    Method that changes user contacts in the Address Book if such user exists.
    :param args: Username and phone that should be stored.
    :return: None.
    """
    name = args[0]
    old_phone = args[1]
    new_phone = args[2]
    rec = contacts.find(name)
    if rec:
        rec.edit_phone(old_phone=old_phone, new_phone=new_phone)
    else:
        raise ValueError(f"The contact with the name '{name}' doesn't exist in the "
                         f"Address Book. Add it first, please.")


@input_error
def find_contact_phone(*args) -> str:
    """
    Method that returns phone number by passed username.
    :param args: Username whose phone number should be shown.
    :return: The string with user's phone number.
    """
    name = args[0]
    rec = contacts.find(name)
    if rec:
        return rec.phones
    else:
        raise ValueError(f"The contact with the name '{name}' doesn't exist in the "
                         f"Address Book.")


@input_error
def show_all(*args) -> str:
    """
    Method that shows all users's phone numbers.
    :return: String with all phone numbers of all users.
    """
    record_num = None
    if args:
        record_num = int(args[0])
    s = "{:^50}".format("***Clients phone numbers***")
    s += "\n{:<10} | {:<20} | {:<300} |\n".format("Number", "User name", "Phone number")
    counter = 1
    records = contacts.iterator(record_num)
    for record_list in records:
        for record in record_list:
            phones_str = ",".join([phone_num.value for phone_num in record.phones])
            s += '{:<10} | {:<20} | {:<30} |\n'.format(counter, record.name.value,
                                                       phones_str)
            counter += 1
        s += "---------------------------+++------------------------------------\n"
    return s


@input_error
def good_bye() -> str:
    """
    Method that returns "Good bye!" string.
    :return: "Good bye!" string.
    """
    return "Good bye!"


@input_error
def show_days_to_birthday(*args) -> str:
    """
    Method returns the number of days to the next client's birthday. The method
    returns the number of days without fractional part.
    :return: String with a number of days.
    """
    name = args[0]
    record = contacts.find(name)
    if record:
        days_to_birthday = record.days_to_birthday()
        return f"Days to the next birthday for the contact '{record.name.value}' is " \
               f"{days_to_birthday} days"
    else:
        raise ValueError(f"Contact with a name '{name}' doesn't exist in the Address "
                         f"Book")


@input_error
def unknown() -> str:
    """
    Method can be called when was typed a command that can't be recognised.
    :return: String with the explanation that was typed incorrect command.
    """
    return "Unknown command. Try again."


COMMANDS = {
    "hello": hello,
    "add": add_contact,
    "change": change_phone,
    "phone": find_contact_phone,
    "show all": show_all,
    "good bye": good_bye,
    "close": good_bye,
    "exit": good_bye,
    "show days to birthday": show_days_to_birthday
}


def main() -> None:
    """
    Method is responsible for creating an endless loop where all additional function is
    calling. The loop can be stopped by passing the appropriate commands (close, exit,
    good bye).
    :return: None.
    """
    while True:
        cli_input = input("Type a command>>> ")
        func_name, func, func_args = parse_cli_command(cli_input)
        print(func(*func_args))
        if func_name in ("good bye", "close", "exit"):
            break


if __name__ == "__main__":
    main()
