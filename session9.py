"""
Module for assignment for session 9
Author: Shilpaj Bhalerao
Date: Jul 06, 2021
"""
# Standard Library Imports
import datetime
import random
from string import ascii_letters
from time import perf_counter
from operator import truediv, mul, add
from collections import namedtuple, Counter
from typing import NamedTuple

# Third-Party Imports
from faker import Faker

# Seeding to ensure same data generation for test cases
fake = Faker()
Faker.seed(0)


def is_namedtuple_instance(instance) -> bool:
    """
    Function to check whether a variable is an instance of a namedtuple
    :param instance: variable to be checked
    :return: True/False
    """
    # Check type and base classes
    _type = type(instance)
    _bases = _type.__bases__

    # Tuple is the parent class of namedtuple so if tuple is not present in bases then return False
    if len(_bases) != 1 or _bases[0] != tuple:
        return False

    # Named-tuples have _fields attributes like dictionary so return False if attributes are not instance of tuples
    fields_ = getattr(_type, '_fields', None)
    if not isinstance(fields_, tuple):
        return False

    return all(type(field) == str for field in fields_)


def generate_profiles(number_of_samples) -> list:
    """
    Function to generate profiles using faker library
    :param number_of_samples: Number of profiles need to be generated
    :return: List of dictionaries(generated profiles)
    """
    print("Generating Profiles ....")
    profiles = []
    [profiles.append(fake.profile()) for i in range(number_of_samples)]
    return profiles


def dictionary_operations(_list_of_dictionaries: list) -> dict:
    """
    Function to calculate the blood type count, mean_location, oldest person age, and average age of all the profiles
    from the sample profiles.
    :param _list_of_dictionaries: list of generated profiles which are of dictionary type
    :return: dictionary of blood group count, mean location, name and age of oldest person, and average age of all
    the profiles
    """
    # Lists, dictionaries and variables to collect the profiles' data which is used for calculations
    _blood_group = []
    x_location = []
    y_location = []
    _days = dict()
    temp_ = dict()
    _index = None
    oldest_days = None

    if isinstance(_list_of_dictionaries, list) and len(_list_of_dictionaries) > 0 and isinstance(_list_of_dictionaries[0], dict):
        for index, profile in enumerate(_list_of_dictionaries):
            for parameter, data in profile.items():
                # Update the blood group data
                if parameter == "blood_group":
                    _blood_group.append(data)

                # Calculate mean current location
                if parameter == "current_location":
                    x_location.append(data[0])
                    y_location.append(data[1])

                # Oldest person age
                if parameter == "birthdate":
                    _days[index] = (datetime.date.today() - data).days
                    oldest_days = max(_days.values())

        # Find the indexes of all the persons with same oldest age in days
        _indexes = [key for key, value in _days.items() if value == oldest_days]
        for _index in _indexes:
            temp_[_list_of_dictionaries[_index]["name"]] = oldest_days

        _blood_group_count = Counter(_blood_group)

        x_mean = truediv(sum(x_location), len(_list_of_dictionaries))
        y_mean = truediv(sum(y_location), len(_list_of_dictionaries))

        # Average age
        avg_age = truediv(sum(_days.values()), len(_list_of_dictionaries))

        output = {'blood_count': _blood_group_count,
                  'mean_location': (x_mean, y_mean),
                  'name_age_of_oldest_person': temp_,
                  'average_age_of_profiles': avg_age}
        return output
    elif type(_list_of_dictionaries) is not list:
        raise TypeError(f"Expected input data is list but received {type(_list_of_dictionaries)}")
    elif len(_list_of_dictionaries) == 0:
        raise ValueError("Enter Valid data. Empty list passed to the function")
    elif type(_list_of_dictionaries[0]) is not dict:
        raise TypeError(f"Enter correct type of data. Data passed is {type(_list_of_dictionaries[0])} and expected "
                        f"data is dictionary")


def namedtuple_operations(list_of_tuples) -> NamedTuple:
    """
    Function to perform operations of namedtuple
    :param list_of_tuples: list of generated profiles in namedtuple datatype
    :return: namedtuple of blood_group_count, mean_location, name_of_oldest_person, age and average age of all profiles
    """
    # Variables for calculations
    _blood_list = []
    x_data = []
    y_data = []
    _days = []

    # Define and add docstring to the output namedtuple
    Output = namedtuple('Output', "blood_group_count mean_location name_of_oldest_person age average_age")
    Output.__doc__ = "NamedTuple for the output of the calculations"
    Output.blood_group_count.__doc__ = "Total number of individuals having respective blood group in the dataset"
    Output.mean_location.__doc__ = "Mean location of all the individuals in the profiles"
    Output.name_of_oldest_person.__doc__ = "Name of the oldest individual in the profiles"
    Output.age.__doc__ = "Age of the oldest individual in days"
    Output.average_age.__doc__ = "Average age of all the individuals in the profiles"

    if len(list_of_tuples) > 0 and is_namedtuple_instance(list_of_tuples[0]) and isinstance(list_of_tuples, list):
        for _tuple in list_of_tuples:
            # Append data to a list to calculate the blood group count
            _blood_list.append(_tuple.blood_group)

            # Append current location (x, y) to the list for mean calculations
            x_data.append(_tuple.current_location[0])
            y_data.append(_tuple.current_location[1])

            # Oldest Person Age
            _days.append((datetime.date.today() - _tuple.birthdate).days)

        # Code to calculate the count of blood group
        _blood_group_count = Counter(_blood_list)

        # Calculations for mean location
        x_mean = truediv(sum(x_data), len(list_of_tuples))
        y_mean = truediv(sum(y_data), len(list_of_tuples))

        # Code to check the name of oldest person
        oldest_days = max(_days)
        oldest_person_names = [list_of_tuples[index].name for index, _day in enumerate(_days) if _day == oldest_days]

        # Average age calculations
        avg_age = truediv(sum(_days), len(list_of_tuples))

        # Create an instance of output namedtuple to return the calculated data
        output = Output(blood_group_count=_blood_group_count,
                        mean_location=(x_mean, y_mean),
                        name_of_oldest_person=oldest_person_names,
                        age=oldest_days,
                        average_age=avg_age)
        return output
    elif type(list_of_tuples) is not list:
        raise TypeError(f"Expected input data is list but received {type(list_of_tuples)}")
    elif len(list_of_tuples) == 0:
        raise ValueError("Enter Valid data. Empty list passed to the function")
    elif not is_namedtuple_instance(list_of_tuples[0]):
        raise TypeError(f"Enter correct type of data. Data passed is {type(list_of_tuples[0])} and expected "
                        f"data is namedtuple")


def compare_namedtuple_and_dictionaries() -> None:
    """
    Function to compare the performance of namedtuples and dictionaries over the 10K profile for same data output
    :return: None
    """
    # Variables used for calculations
    list_of_named_tuples = []

    # Generate 10K profiles
    list_of_dictionaries = generate_profiles(10_000)

    # Perform operations on the dictionary
    start = perf_counter()
    _ = dictionary_operations(list_of_dictionaries)
    elapsed_dict = perf_counter() - start
    print("Output: ", _)
    print("Operation Time on Dictionary: ", elapsed_dict)
    print()

    # Sample profile to create named tuple fields
    sample_profile = list_of_dictionaries[1]

    # Create and add docstring to the namedtuple profile
    PersonProfile = namedtuple('PersonProfile', sorted(sample_profile.keys()))
    PersonProfile.__doc__ = "Profile of an individual containing data associated with that individual"
    PersonProfile.address.__doc__ = "Address of an individual in String format"
    PersonProfile.birthdate.__doc__ = "Date of birth of an individual in datetime.date(year, month, day) format"
    PersonProfile.blood_group.__doc__ = "Blood group of an individual in String format"
    PersonProfile.company.__doc__ = "Name of a company with which an individual is associated with in String format"
    PersonProfile.current_location.__doc__ = "Current location of an individual in tuple of Decimals format"
    PersonProfile.job.__doc__ = "Job of an individual in String format"
    PersonProfile.mail.__doc__ = "Email address of an individual in String format"
    PersonProfile.name.__doc__ = "Name of an individual in String format"
    PersonProfile.residence.__doc__ = "Residence of an individual in String format"
    PersonProfile.sex.__doc__ = "Gender of an individual in String format"
    PersonProfile.ssn.__doc__ = "Social Security Number of an individual in String format"
    PersonProfile.username.__doc__ = "Username of an individual in String format"
    PersonProfile.website.__doc__ = "Websites of an individual in list of String format"

    # Create a list of named tuple
    [list_of_named_tuples.append(PersonProfile(**profile)) for profile in list_of_dictionaries]
    print(list_of_named_tuples[0])
    print()

    # Perform same operations on the namedtuple
    start = perf_counter()
    _ = namedtuple_operations(list_of_named_tuples)
    elapsed_named_tuple = perf_counter() - start
    print("Output: ", _)
    print("Operation Time on NamedTuples: ", elapsed_named_tuple)

    print()
    print(f"Tuples are faster than dictionaries by {elapsed_dict / elapsed_named_tuple} times")

# ---------------------------------------------------------------------------------------------------------------------


def generate_price(share_price, percentage_change, high=False):
    """
    Function to generate prices of the share
    :param high: True to generate the highest price of the stock
    :param share_price: Random price of a share
    :param percentage_change: Maximum percentage change in share price
    :return: share price
    """
    delta = mul(truediv(percentage_change, 100), share_price)
    if high:
        return share_price + delta
    else:
        stock_price = random.randint(int(share_price - delta), int(share_price + delta))
        return stock_price


def generate_stock_data(number_of_companies):
    """
    Function to generate stock data for 100 companies
    :param number_of_companies: number of companies for which data is generated
    :return: NamedTuple with fields - name, symbol, open, high, close
    """
    _list_of_companies = []
    market_percentage_fluctuation = 5
    share_min_price = 100
    share_max_price = 2000
    symbol_length = 3
    _list_of_market_cap = []
    _list_of_company_symbol = []

    CompanyStock = namedtuple('CompanyStock', "name symbol open high close market_cap company_weight",
                              defaults=[None] * 7)
    CompanyStock.__doc__ = "Stock information for a company"
    CompanyStock.name.__doc__ = "Name of the company"
    CompanyStock.symbol.__doc__ = "Symbol of the company"
    CompanyStock.open.__doc__ = "Opening share price of the company"
    CompanyStock.high.__doc__ = "Highest share price of the company for the day"
    CompanyStock.close.__doc__ = "Closing share price of the company"
    CompanyStock.market_cap.__doc__ = "Market capital of the company"
    CompanyStock.company_weight.__doc__ = "Weight of the company on stock exchange"

    for i in range(number_of_companies):
        # Generate company name
        company_name = fake.company()

        # Generate company symbol
        company_symbol = company_name[0:symbol_length].upper()
        company_symbol = company_symbol.replace(' ', random.choice(ascii_letters))
        company_symbol = company_symbol.replace(',', random.choice(ascii_letters))
        _list_of_company_symbol.append(company_symbol)

        # Generate a random market_cap for the company
        company_market_cap = random.randint(1_000_000, 1_000_000_000)
        _list_of_market_cap.append(company_market_cap)

        # Opening price of company's stock
        company_open_price = generate_price(random.randint(share_min_price, share_max_price),
                                            random.randint(0, market_percentage_fluctuation))

        # High price of company's stock
        company_high_price = generate_price(company_open_price, market_percentage_fluctuation, high=True)

        # Closing price of company's stock
        company_close_price = generate_price(company_open_price, random.randint(0, market_percentage_fluctuation))

        company = CompanyStock(name=company_name, symbol=company_symbol, open=company_open_price,
                               high=company_high_price, close=company_close_price, market_cap=company_market_cap,
                               company_weight=None)

        # Append the stock data in namedtuple format
        _list_of_companies.append(company)

    _opening_market_value = sum(_list_of_market_cap)
    _list_of_companies = [company._replace(company_weight=(company.market_cap / _opening_market_value)) for company in _list_of_companies]

    return _list_of_companies, _opening_market_value, _list_of_company_symbol


def stock_market_():
    """
    Generate one instance of the market and calculate the change in the market points
    :return:
    """
    # Variables used for the code
    _market_trades = []
    _new_market_value = []

    # Generate the stock data in namedtuple format for 100 companies
    list_of_companies, opening_market_value, list_of_company_symbol = generate_stock_data(100)

    for _company in list_of_companies:
        new_company_value = add(_company.market_cap, truediv(mul(_company.market_cap, random.randint(-10, 10)), 100))
        _new_market_value.append(new_company_value)

    print(f"Opening Market Value: {opening_market_value}")
    print(f"New Values: {_new_market_value}")
    current_market_value = sum(_new_market_value)
    print(f"Current Market Value: {current_market_value}")
    market_change_in_points = (current_market_value - opening_market_value) / opening_market_value
    print(f"Change: {100 + (market_change_in_points * 100)}")


if __name__ == '__main__':
    # Part one of comparing performance of named-tuples and dictionaries
    compare_namedtuple_and_dictionaries()

    # Part two of generating stock data
    stock_market_()
