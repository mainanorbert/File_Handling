# Data Integration Project
This project aims to read data from different types of files (CSV, JSON, XML), process and combine them, and then map the combined data to a MySQL database using Pony ORM.
The goal is to provide a unified view of the data from various sources in a structured format in the database.
# How to Use
## Prerequisites

### Programs
- Python 3.x
- [pony.orm](#Setup)
- MySQL database
[How to install Myql Database](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04)

### Files to use
- csv (For test use `user_data_23_4.csv` in the project directory)
- json (For test use `user_data_23_4.xml` in the project directory)
- xml.etree.ElementTree (For test use `user_data_23_4.xml` in the project directory)

## Setup the Project
To set up the project and run it locally:
1. Clone repository:
   ```sh
   git clone https://github.com/mainanorbert/File_Handling.git
2. Navigate into the repository:
   ```sh
   cd File_Handling
3. Install Virtual environment:
   ```sh
   python3 -m venv .venv
4. Activate Virtual Environment
   ```sh
   . .venv/bin/activate
5. install Mysqlclient
   ```sh
   pip install mysqlclient
6. install ponyorm
   ```sh
   pip install pony
7. Run the program
   ```sh
   python3 File_Integration_function

- The progran will generate `combined_data.json` containing combined data from json, xml, and csv files
- The program will also save the combined data to your mysql database `customer_data`. in line 133 of the code, remember to provide the credentials for the program to access the database
