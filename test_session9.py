"""
Test cases for functions in session9.py
Author: Shilpaj Bhar
Date: Jul 06, 2021
"""
# Standard Library Imports
import pytest
from statistics import mean
from decimal import Decimal
from datetime import date
from typing import NamedTuple
from dateutil.relativedelta import relativedelta

# Third-Party Imports
from faker import Faker

# Local Imports
from session9 import *

fake = Faker()
Faker.seed(1)


def test_generate_profiles_of_sample_size():
    """
    Test case to check the generated data
    """
    required_keys = ['job', 'company', 'ssn', 'residence', 'current_location', 'blood_group',
                     'website', 'username', 'name', 'sex', 'address', 'mail', 'birthdate']

    # Generate 10 samples
    profiles = generate_profiles(10)

    # Check if 10 samples are generated
    assert 10 == len(profiles)

    # Check if type of each sample is dictionary
    _conditions = [type(sample) is dict for sample in profiles]
    assert (all(_conditions))

    # Check if all the required keys are present in the generated data
    _checks = [list(sample.keys()) == required_keys for sample in profiles]
    assert (all(_checks))


def test_dictionary_operations_wrong_input():
    """
    Test to check if appropriate exceptions are raised if no data is passed or wrong type of data is passed
    """
    # Test for empty list
    empty_list = []
    with pytest.raises(ValueError):
        dictionary_operations(empty_list)

    # List with wrong type of data
    a = range(10)
    b = range(11, 21)
    with pytest.raises(TypeError):
        dictionary_operations([a, b])

    # Tuple as a input with correct data
    data_1 = fake.profile()
    data_2 = fake.profile()
    with pytest.raises(TypeError):
        dictionary_operations((data_1, data_2))


def test_dictionary_operations_output():
    """
    Test case to check the correct output for a unit case of 2 profiles
    """
    expected_output = {'blood_count': Counter({'B+': 1, 'AB+': 1}),
                       'mean_location': (Decimal('63.1813715'), Decimal('84.5430095')),
                       'name_age_of_oldest_person': {'Veronica Maldonado': 32983},
                       'average_age_of_profiles': 18364.0}
    data_1 = fake.profile()
    data_2 = fake.profile()
    output = dictionary_operations([data_1, data_2])
    print()
    print(f"Expected output: {expected_output}")
    print()
    print(f"Actual output: {output}")

    assert expected_output == output


def test_dictionary_operations_blood_count():
    """
    Test to check the correct count of blood group and raise error if wrong blood_group is passed
    """
    # Create a list of 10 profiles
    list_of_10_dicts = []
    [list_of_10_dicts.append(fake.profile()) for i in range(10)]

    # Replace all the blood groups by 'B+' in all the profiles
    for _dict in list_of_10_dicts:
        for key, value in _dict.items():
            if key == 'blood_group':
                _dict[key] = 'B+'

    # Check if the calculations show the correct count
    output = dictionary_operations(list_of_10_dicts)
    assert 10 == output['blood_count']['B+']


def test_dictionary_operations_mean_location():
    """
    Test to check correct mean location data
    """
    x_mean = []
    y_mean = []

    # Create a list of 10 profiles
    list_of_10_dicts = []
    [list_of_10_dicts.append(fake.profile()) for i in range(10)]

    # Gather all x, y data to calculate mean using statistics
    for index, _dict in enumerate(list_of_10_dicts):
        for key, value in _dict.items():
            if key == 'current_location':
                x_mean.append(_dict[key][0])
                y_mean.append(_dict[key][1])

    _stats_mean = (mean(x_mean), mean(y_mean))

    # Check if the calculations show the correct mean compared with the statistics mean
    output = dictionary_operations(list_of_10_dicts)
    assert _stats_mean == output['mean_location']


def test_dictionary_operations_age():
    """
    Test to check correct oldest person and output when two people of same age are oldest/non-oldest
    """
    # Create a list of 10 profiles
    list_of_10_dicts = []
    [list_of_10_dicts.append(fake.profile()) for i in range(10)]

    output = dictionary_operations(list_of_10_dicts)
    assert len(output['name_age_of_oldest_person']) == 1

    # Replace everyone's birthdate as Jan 1, 1800
    for index, _dict in enumerate(list_of_10_dicts):
        for key, value in _dict.items():
            if key == 'birthdate':
                _dict[key] = datetime.date(1800, 1, 1)

    # Check the oldest_age shows age of all of them
    output = dictionary_operations(list_of_10_dicts)
    assert len(output['name_age_of_oldest_person']) == 10


def test_dictionary_operations_avg_age():
    """
    Test to check the correct average age of the group
    """
    # Create a list of 10 profiles
    list_of_10_dicts = []
    [list_of_10_dicts.append(fake.profile()) for i in range(10)]

    # Replace everyone's birthdate as Jan 1, 1800
    for index, _dict in enumerate(list_of_10_dicts):
        for key, value in _dict.items():
            if key == 'birthdate':
                _dict[key] = datetime.date(1800, 1, 1)

    # Calculate current age
    age = date.today() - date(1800, 1, 1)

    # Check the oldest_age shows age of all of them
    output = dictionary_operations(list_of_10_dicts)

    print(f"Calculated Average age: {output['average_age_of_profiles']} and since everyone's birthdate is same, "
          f"current age of {age.days} days should be average age")
    assert output['average_age_of_profiles'] == age.days


def test_namedtuple_docstring():
    """
    Test to check the namedtuple docstrings
    """
    data = []
    list_of_named_tuples = []

    [data.append(fake.profile()) for i in range(10)]
    PersonProfile = namedtuple('person_profile', sorted(data[0].keys()))
    [list_of_named_tuples.append(PersonProfile(**profile)) for profile in data]
    print(list_of_named_tuples[0].__class__.__base__.__name__)
    output = namedtuple_operations(list_of_named_tuples)

    assert 'NamedTuple for the output of the calculations' in output.__doc__
    assert 'Alias for field number' not in type(output).blood_group_count.__doc__
    assert 'Alias for field number' not in type(output).mean_location.__doc__
    assert 'Alias for field number' not in type(output).name_of_oldest_person.__doc__
    assert 'Alias for field number' not in type(output).age.__doc__
    assert 'Alias for field number' not in type(output).average_age.__doc__


def test_namedtuple_input_data():
    """
    Test to check type of input data
    """
    # Test for empty list
    empty_list = []
    with pytest.raises(ValueError):
        namedtuple_operations(empty_list)

    # List with wrong type of data
    a = range(10)
    b = range(11, 21)
    with pytest.raises(TypeError):
        namedtuple_operations([a, b])

    # Tuple as a input with correct data
    data_1 = fake.profile()
    data_2 = fake.profile()
    with pytest.raises(TypeError):
        namedtuple_operations((data_1, data_2))


def test_namedtuple_blood_count():
    """
    Test to check the correct count of blood group and raise error if wrong blood_group is passed for named-tuple
    """
    # Lists used for calculations in this scope
    modified_list = []
    list_of_named_tuples = []

    # Generate 10K profiles
    list_of_dictionaries = generate_profiles(10)
    PersonProfile = namedtuple('PersonProfile', sorted(list_of_dictionaries[0].keys()))

    # List of named tuple
    for profile in list_of_dictionaries:
        list_of_named_tuples.append(PersonProfile(**profile))

    for _namedtuple in list_of_named_tuples:
        modified_list.append(_namedtuple._replace(blood_group='B+'))

    output = namedtuple_operations(modified_list)
    assert 10 == output.blood_group_count['B+']


def test_namedtuple_mean_location():
    """
    Test to check correct mean location data for named-tuples
    """
    # Lists used for calculations in this scope
    modified_list = []
    list_of_named_tuples = []

    # Generate 10K profiles
    list_of_dictionaries = generate_profiles(10)
    PersonProfile = namedtuple('PersonProfile', sorted(list_of_dictionaries[0].keys()))

    # List of named tuple
    for profile in list_of_dictionaries:
        list_of_named_tuples.append(PersonProfile(**profile))

    for index, _namedtuple in enumerate(list_of_named_tuples):
        modified_list.append(_namedtuple._replace(current_location=(index, index)))

    output = namedtuple_operations(modified_list)
    assert (4.5, 4.5) == output.mean_location


def test_namedtuple_oldest_person():
    """
    Test to check correct oldest person and output when two people of same age are oldest/non-oldest for named-tuples
    """
    # Lists used for calculations in this scope
    modified_list = []
    profile_names = []
    list_of_named_tuples = []

    # Generate 10K profiles
    list_of_dictionaries = generate_profiles(10)
    PersonProfile = namedtuple('PersonProfile', sorted(list_of_dictionaries[0].keys()))

    # List of named tuple
    for profile in list_of_dictionaries:
        list_of_named_tuples.append(PersonProfile(**profile))

    for index, _namedtuple in enumerate(list_of_named_tuples):
        modified_list.append(_namedtuple._replace(birthdate=datetime.date(1800, 1, 1)))
        profile_names.append(_namedtuple.name)

    output = namedtuple_operations(modified_list)
    assert profile_names == output.name_of_oldest_person


def test_namedtuple_average_age():
    """
    Test to check the correct average age of the group
    """
    modified_list = []
    list_of_named_tuples = []

    # Generate 10K profiles
    list_of_dictionaries = generate_profiles(10)
    PersonProfile = namedtuple('PersonProfile', sorted(list_of_dictionaries[0].keys()))

    # List of named tuple
    for profile in list_of_dictionaries:
        list_of_named_tuples.append(PersonProfile(**profile))

    for index, _namedtuple in enumerate(list_of_named_tuples):
        modified_list.append(_namedtuple._replace(birthdate=datetime.date(1800, 1, 1)))

    output = namedtuple_operations(modified_list)
    assert (date.today() - date(1800, 1, 1)).days == output.average_age


def test_speed():
    """
    Test to check the execution speed of named-tuples and dictionaries to prove that named-tuples are faster
    """
    # Variables used in this scope
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

    # Sample profile to create named tuple
    sample_profile = list_of_dictionaries[1]

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

    # List of named tuple
    [list_of_named_tuples.append(PersonProfile(**profile)) for profile in list_of_dictionaries]
    print(list_of_named_tuples[0])
    print()

    # Perform operations on the dictionary
    start = perf_counter()
    _ = namedtuple_operations(list_of_named_tuples)
    elapsed_named_tuple = perf_counter() - start
    print("Output: ", _)
    print("Operation Time on NamedTuples: ", elapsed_named_tuple)

    print()
    print(f"Tuples are faster than dictionaries by {elapsed_dict / elapsed_named_tuple} times")

    assert elapsed_named_tuple < elapsed_dict


def test_stock_data_generation():
    """
    Test case to check if the company stock data is generated
    """
    # Generate the stock data in namedtuple format for 100 companies
    list_of_companies, opening_market_value, list_of_company_symbol = generate_stock_data(100)

    assert len(list_of_companies) == 100


def test_datatype_of_stock_data():
    """
    Test case to check the datatype of the stock data
    """
    # Generate the stock data in namedtuple format for 100 companies
    list_of_companies, opening_market_value, list_of_company_symbol = generate_stock_data(100)

    assert is_namedtuple_instance(list_of_companies[0])


def test_docstring_of_generated_data():
    """
    Test case to check if the generated namedtuple data has docstring
    """
    # Generate the stock data in namedtuple format for 100 companies
    list_of_companies, opening_market_value, list_of_company_symbol = generate_stock_data(100)

    sample_data = list_of_companies[0]
    assert 'Stock information for a company' in sample_data.__doc__
    assert 'Alias for field number' not in type(sample_data).name.__doc__
    assert 'Alias for field number' not in type(sample_data).symbol.__doc__
    assert 'Alias for field number' not in type(sample_data).open.__doc__
    assert 'Alias for field number' not in type(sample_data).high.__doc__
    assert 'Alias for field number' not in type(sample_data).close.__doc__
    assert 'Alias for field number' not in type(sample_data).market_cap.__doc__
    assert 'Alias for field number' not in type(sample_data).company_weight.__doc__


def test_high_with_opening_and_closing_value():
    """
    Test case to check all the high values are greater than or equal to opening value and closing value
    """
    # Generate the stock data in namedtuple format for 100 companies
    list_of_companies, opening_market_value, list_of_company_symbol = generate_stock_data(100)

    _conditions = [(company.high >= company.open) and (company.high >= company.close) for company in list_of_companies]

    assert all(_conditions) is True


def test_required_fields():
    """
    Test case to check if all the required fields are present in the generated data
    """
    # Expected fields
    expected_fields = ('name', 'symbol', 'high', 'open', 'close')

    # Generate the stock data in namedtuple format for 100 companies
    list_of_companies, opening_market_value, list_of_company_symbol = generate_stock_data(100)

    sample_data = list_of_companies[0]
    current_fields = sample_data._fields

    conditions = [True for field in expected_fields if field in current_fields]
    assert all(conditions) is True


def test_symbols():
    """
    Test case to check if all the symbols are 3 capitalize alphabets without spaces and commas
    """
    # Generate the stock data in namedtuple format for 100 companies
    list_of_companies, opening_market_value, list_of_company_symbol = generate_stock_data(100)

    conditions = [True for company in list_of_companies if company.symbol.isupper() and ',' not in company.symbol and ' ' not in company.symbol]

    assert all(conditions) is True


def test_weights_eq_one():
    """
    Test case to check if all the companies are weighted properly that is there sum of their weights is one
    """
    # Generate the stock data in namedtuple format for 100 companies
    list_of_companies, opening_market_value, list_of_company_symbol = generate_stock_data(100)

    weights = []
    [weights.append(company.company_weight) for company in list_of_companies]

    assert round(sum(weights)) == 1


def test_market_up_condition():
    """
    Test case to check points output if all the company's stocks are up by 10%
    """
    # Variables used for code flow in this scope
    _new_market_value = []

    # Generate the stock data in namedtuple format for 100 companies
    list_of_companies, opening_market_value, list_of_company_symbol = generate_stock_data(100)

    for _company in list_of_companies:
        new_company_value = add(_company.market_cap, truediv(mul(_company.market_cap, 10), 100))
        _new_market_value.append(new_company_value)

    current_market_value = sum(_new_market_value)
    assert current_market_value > opening_market_value


def test_market_down_condition():
    """
    Test case to check points output if all the company's stocks are down by 10%
    """
    # Variables used for code flow in this scope
    _new_market_value = []

    # Generate the stock data in namedtuple format for 100 companies
    list_of_companies, opening_market_value, list_of_company_symbol = generate_stock_data(100)

    for _company in list_of_companies:
        new_company_value = add(_company.market_cap, truediv(mul(_company.market_cap, -10), 100))
        _new_market_value.append(new_company_value)

    current_market_value = sum(_new_market_value)
    assert current_market_value < opening_market_value


def test_points_up_condition():
    """
    Test case to check if all the stocks are up by 20% then how much points are added to the market
    """
    # Variables used for code flow in this scope
    _new_market_value = []

    # Generate the stock data in namedtuple format for 100 companies
    list_of_companies, opening_market_value, list_of_company_symbol = generate_stock_data(100)

    for _company in list_of_companies:
        new_company_value = add(_company.market_cap, truediv(mul(_company.market_cap, 20), 100))
        _new_market_value.append(new_company_value)

    current_market_value = sum(_new_market_value)
    market_change_in_points = (current_market_value - opening_market_value) / opening_market_value

    assert 120 == round(100 + (market_change_in_points * 100))
