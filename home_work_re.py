# flags just for testing
# set to True, when you want recieve test results
test_first_task = False
test_second_task = False
test_third_task = False
test_forth_task = True

# ------------------------------------------------------------
# First task
# ------------------------------------------------------------
def get_days_from_today(date: str) -> int:    
    """
    Calculate amount of days between 'date' and current date

    Args:
        date: date in string in 'YYYY-MM-DD' format
    Returns:
        int: amount of days
    """
    from datetime import datetime
    import re

    # check date format with regular expression
    # want to make some practise
    pattern = r"^(?:19|20)[0-9]{2}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12][0-9]|3[01])$"
    check_format = re.fullmatch(pattern=pattern, string=date)
    if not check_format:
        raise ValueError("Date must be 'YYYY-MM-DD'")
    
    # but we cant handle 31 Feb :(
    # simpliest way to use try/except    
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError as e:
        raise ValueError("Date must be a valid calendar date") from e

    today = datetime.today().date()
    delta = today - date_obj

    return delta.days

if test_first_task:
    print("-"*50)
    print("Task 1:")
    date = input ("Enter date in format YYYY-MM-DD: ")
    print(get_days_from_today(date))
    print("-"*50)
    
# ------------------------------------------------------------
# Second task
# ------------------------------------------------------------

def get_numbers_ticket(min_lottery: int, max_lottery: int, quantity: int) -> list:
    """
    Generate a list of unique random numbers within a given range.

    Args:
        min_lottery: Minimum value (inclusive)
        max_lottery: Maximum value (inclusive)
        quantity: Number of unique random numbers to generate

    Returns:
        list: List of unique random numbers
    """
    import random
    
    result = []   
    # NOTE: Навмисно використовую print лише для навчальної демонстрації причин відмови.
    # В умовах таски потрібно повертати пустий список при помилці :((
    # У продакшн-коді друк у функціях не використовуємо (винятки або повернення коду помилки).
    
    # we check all parameters and raise flag, when its problem
    parameters_is_good = True
    if min_lottery < 1:
        print("Minimum value must be 1 or greater")
        parameters_is_good = False
    elif max_lottery > 1000:
        print("Maximum value must be less then 1 000")
        parameters_is_good = False
    elif min_lottery > max_lottery:
        print("Maximum value must be equal or greater then min")
        parameters_is_good = False
    elif quantity > (max_lottery - min_lottery + 1):
        print("Quantity must not exceed range between min and max")
        parameters_is_good = False
    elif quantity < 1:
        print("Quantity must be at least 1")
        parameters_is_good = False
    
    # return empty list when we have troubles
    if not parameters_is_good:
        return result
        
    result = random.sample(range(min_lottery, max_lottery+1), quantity)
    result.sort()

    return result

if test_second_task:
    print("-"*50)
    print("Task 2:")
    min = int(input("Enter min lottery number >>> "))
    max = int(input("Enter max lottery number >>> "))
    qty = int(input("Enter quantity of lottery numbers >>> "))
    lottery_numbers = get_numbers_ticket(min, max, qty) # 1, 49, 6
    print("Ваші лотерейні числа:", lottery_numbers)
    print("-"*50)


# ------------------------------------------------------------
# Third task
# ------------------------------------------------------------
def normalize_phone(phone_number: str) -> str:
    """
    Normalize ukrainian phone number in +380XXXXXXXXX format.

    Args:
        phone_number: unnormalized phone number

    Returns:
        string: normalized phone number or error message
    """
    import re

    # remove all except digits
    phone_number = re.sub(r"[^0-9]","",phone_number)
    if len(phone_number) == 12 and phone_number.startswith("380"):
        return "+" + phone_number
    elif len(phone_number) == 10:
        return "+38" + phone_number
    else:
        return "Wrong ukrainian phone number"


if test_third_task:
    raw_numbers = [
        "067\\t123 4567",
        "(095) 234-5678\\n",
        "+380 44 123 4567",
        "380501234567",
        "    +38(050)123-32-34",
        "     0503451234",
        "(050)8889900",
        "38050-111-22-22",
        "38050 111 22 11   ",
    ]

    sanitized_numbers = [normalize_phone(num) for num in raw_numbers]
    print("Нормалізовані номери телефонів для SMS-розсилки:", sanitized_numbers)    

    raw_numbers = [
        "067\\t123 4567_11",
        "(095) 234-56",
        "+44 44 123 4567",
        "+80501234567",
    ]

    sanitized_numbers = [normalize_phone(num) for num in raw_numbers]
    print("Нормалізовані номери телефонів для SMS-розсилки:", sanitized_numbers)      

# ------------------------------------------------------------
# Forth task
# ------------------------------------------------------------
def get_upcoming_birthdays(users: list) -> list:
    """
    Determines the upcoming birthdays within the next 7 days from a list of users 
    and adjusts the congratulation date to avoid weekends.
    Args:
        users (list): A list of dictionaries, where each dictionary contains:
            - "name" (str): The name of the user.
            - "birthday" (str): The user's birthday in the format "YYYY.MM.DD".
    Returns:
        list: A list of dictionaries, where each dictionary contains:
            - "name" (str): The name of the user.
            - "congratulation_date" (str): The adjusted congratulation date in the format "YYYY.MM.DD".
              If the birthday falls on a Saturday, the congratulation date is moved to the following Monday.
              If the birthday falls on a Sunday, the congratulation date is moved to the following Monday.
              29-02 moved to 28-02
    """


    from datetime import datetime, timedelta, date
    
    result = []
    today = datetime.today().date()
    
    for user in users:
        birthday_date = datetime.strptime(user["birthday"], "%Y.%m.%d").date()
        
        # try.. except for 29.02 cases
        try:
            birthday_date = birthday_date.replace(year=today.year)
        except ValueError:
            birthday_date = date(today.year, 2, 28)

        delta = (birthday_date - today).days
        # if bithday passed we need to use next year
        if delta < 0:
            birthday_date = birthday_date.replace(year=today.year+1)
            delta = (birthday_date - today).days
        if delta >=0 and delta <=7:
            congratulation_date = birthday_date
            if birthday_date.weekday() == 5:
                congratulation_date = congratulation_date + timedelta(days=2)
            elif birthday_date.weekday() == 6:
                congratulation_date = congratulation_date + timedelta(days=1)
            result.append({"name": user["name"], "congratulation_date": congratulation_date.strftime("%Y.%m.%d")})
    
    return result

if test_forth_task:
    users = [
        {"name": "John Doe", "birthday": "1985.01.23"},
        {"name": "Jane Smith", "birthday": "1990.01.27"},
        {"name": "Rembo", "birthday": "1590.10.10"},
        {"name": "Robocop", "birthday": "1590.10.05"},
        {"name": "Terminator", "birthday": "2000.10.12"},
        {"name": "Just one guy", "birthday": "2000.10.04"},
    ]

    upcoming_birthdays = get_upcoming_birthdays(users)
    print("Список привітань на цьому тижні:", upcoming_birthdays)    