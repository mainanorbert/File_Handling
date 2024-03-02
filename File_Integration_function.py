#!/usr/bin/python3
import csv
import json
import xml.etree.ElementTree as ET
from pony.orm import Database, Optional, Required, db_session


"""This code is for reading data from various types of files"""
# Function to extract data from CSV file
def extract_csv(file_path):
    """extracts data from csv file"""
    try:
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            data = [row for row in csv_reader]
        return data
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None
# extracting data from json file
def extract_json(file_path):
    """Function to extract data from JSON file"""
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
        for item in data:
            if 'debt' in item:
                try:
                    x = float(item['debt'])                 
                    item['debt_amount'] = item['debt']
                except:              
                    item['debt_amount'] = item['debt']['amount']
                    item['debt_period_in_years'] = item['debt']['time_period_years']
                finally:
                    del item['debt']
        return data
    
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return None
# extracting data from txt file
def extract_txt(file_path):
    """ Function to extract data from text file"""
    try:
        with open(file_path, 'r') as txt_file:
            data = [line.strip() for line in txt_file]
        return data
    except Exception as e:
        print(f"Error reading TXT file: {e}")
        return None
# extracting data from xml file
def extract_xml(file_path):
    """ Function to extract data from XML file"""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        data = []
        for user_elem in root.findall('.//user'):
            record_data = {}
            for attr_name, attr_value in user_elem.attrib.items():
                record_data[attr_name] = attr_value
            data.append(record_data)
        return data
    except Exception as e:
        print(f"Error reading XML file: {e}")
        return None
    

"""This section is where data is compaired filtered for inconsistencies and combined save into a Json file"""
customer_details_file = "user_data_23_4.json"
customer_vehicle_file = "user_data_23_4.csv"
customer_info_file = "user_data_23_4.xml"
print("reading from files data...")
customer_details = extract_json(customer_details_file)
customer_vehicle = extract_csv(customer_vehicle_file)
customer_info = extract_xml(customer_info_file)
print("read success!")


def combine(file_name):
    """
    checks for inconsistencies in the data user (json file) and vehicle data (csv) if there are any inconsistencies it will remove the data from the list and return the combined data
    """
    with open(file_name + ".json", 'w', newline='') as combine:
        json_data = []
        print("checking for inconsistencies...")
        for i in range(len(customer_details)):
            First_Name = customer_details[i]['firstName']
            Second_Name = customer_details[i]['lastName']
            age = customer_details[i]['age']

            for x in range(len(customer_vehicle)):
                '''check whether the first name, second name and age are the same in both the files'''
                if (First_Name != customer_vehicle[x]['First Name']
                    and Second_Name != customer_vehicle[x]['Second Name']
                    and age != customer_vehicle[x]['Age (Years)']):
                    continue
                else:
                    customer_details[i]['Sex'] = customer_vehicle[x]['Sex']
                    customer_details[i]['Vehicle_Make']= customer_vehicle[x]['Vehicle Make']
                    customer_details[i]['Vehicle_Model'] = customer_vehicle[x]['Vehicle Model']
                    customer_details[i]['Vehicle_Year'] = customer_vehicle[x]['Vehicle Year']
                    customer_details[i]['Vehicle_Type'] = customer_vehicle[x]['Vehicle Type']
                    
                    """json_data.append(employee_data[employee])"""
            for y in range(len(customer_info)):
                if (First_Name != customer_info[y]['firstName'] and Second_Name != customer_info[y]['lastName'] and age != customer_info[y]['age'] and 
                    customer_details[i]['Sex'] != customer_info[y]['sex']):
                    continue
                else:
                    customer_details[i]['Retired'] = customer_info[y]['retired']
                    customer_details[i]['Dependants'] = customer_info[y]['dependants']
                    customer_details[i]['Marital_Status'] = customer_info[y]['marital_status']
                    customer_details[i]['Salary'] = customer_info[y]['salary']
                    customer_details[i]['Pension'] = customer_info[y]['pension']
                    customer_details[i]['Company'] = customer_info[y]['company']
                    customer_details[i]['Commute_Distance'] = customer_info[y]['commute_distance']
                    customer_details[i]['Address_Code'] = customer_info[y]['address_postcode']
            json_data.append(customer_details[i])
        json.dump(json_data, combine, indent=4)
    print("inconsitency check complete!")
    return True 

print("combining data...")
combine("combined_data")
print("data succesfully combined! check combined_data.json")

""" After the data has been filtered for incosistencies it is mapped in the database using ponyORM""" 
print("Mapping combined data to database...")
db = Database()
# Set the MySQL database connection string
db.bind(provider='mysql', host='localhost', user='mainanorbert', passwd='pope@2019', db='customer_data')

class Customer(db.Entity):
    """Defining a class entity for customer fields"""
    __table__ = 'Customers'
    firstName = Required(str)
    lastName = Required(str)
    age = Required(int)
    iban = Required(str)
    credit_card_number = Required(str)
    credit_card_security_code = Required(str)
    credit_card_start_date = Required(str)
    credit_card_end_date = Required(str)
    address_main = Required(str)
    address_city = Required(str)
    address_postcode = Required(str)
    Sex = Required(str)
    Vehicle_Make = Required(str)
    Vehicle_Model = Required(str)
    Vehicle_Year = Required(str)
    Vehicle_Type = Required(str)
    Retired = Required(str)
    Dependants = Required(str)
    Marital_Status = Required(str)
    Salary = Required(str)
    Pension = Required(str)
    Company = Required(str)
    Commute_Distance = Required(str)
    Address_Code = Required(str)
    debt_amount = Optional(str, nullable=True)
    debt_period_in_years = Optional(int, nullable=True)

# Generate the database schema
db.generate_mapping(create_tables=True)

with open("combined_data.json", 'r') as json_file:
    json_data = json.load(json_file)
# Insert data into the MySQL database
    with db_session:
        for data in json_data:
            Customer(**data)

# Commit changes to the database
db.commit()
print("data succesfully mapped to database")
