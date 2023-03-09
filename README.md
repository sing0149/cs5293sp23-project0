## cs5293sp23-project0

## Name: Sagar Singh

## Requirements
Python 3.7 or above
PyPDF2 module
SQLite3 library
Requests library

## Installations
1. Install python 3.7 or above
2. pip install PyPDF2
3. pip install requests
or 
4. Install all the required libraries using "pip install -r requirements.txt"

## Running the project
1. Clone the repository to local machine , or download the file in ZIP format and extract it.
2. Open terminal and navigate to the directory with the code.
3. Run the command "python main.py --incidents <url>" 
4. The code will fetch the PDF and extract / store the relevant data.
4. It will then display the count of incidents by their nature.


## Assumptions made before writing the logic
- The file  to be fetched is in pdf format.
- The pdf consists of multiple pages.
- The incident date/time is in MM/DD/YYYY HH:MM format,i have wrote regular expression to match this pattern.
- The structure of PDF is replicated to a table containing 5 coloumns.
- The nature field is either EMSSTAT, a five-digit number, or a nine-digit number starting with OK.
- The incident ORI field is either EMSSTAT, a five-digit number, or a nine-digit number starting with OK.



## External libraries and modules used
1. re : this was used to support regular expression to match patterns in the extracted file .
2. Sqlite 3: This module is used to create and insert values in the databsed.
3. requests : This module was used to send HTTP requests.It fetches the pdf file from the given url.
4. IO : This module was used to create an input stream for PyPDF2.
5. typing : this is used in the code to mention the data types of i/0 param of the functions.



## Functions used in the project

1. main():
- main function is located in the main.py file, which basically have the driver code . Functions are called in the main function. The URL entered in the command line will be passed into this funtion.

2. fetchincidents():
- this function takes the url as input and returns the file data in bytes format
- it also sets a user agent header to imitate a browser and get rid of user agent filtering


3. extractincidents():
- This function takes the binary data returned by fetchincidents() as an input adn returns a list of lists that contains incident data. 
- It uses PyPDF2 to extract text from binary data PDF
- It  pertains RE for pattern matching to extract specific fields like time , nature , ori etc. 
- It process every page in pdf file and adds every incident to the list of incidents

4. createdb():
- this function creates a database named "normanpd.db",and creates table named "incidents" in it.The table consists of 5 coloumns i.e. incident time,incident number,incident location, nature and incident ori. 
- It returns a connection to the database

5. populatedb(db,processed_data):
- This takes db connection object and list of incidents as input and then inserts that data into the table of normanpd.db using SQL query. It commits the changes to the database.

6. status(db):
- it takes db connection object as input and runs a query to fetch the number of incidents by nature and print results separated by "|". 
-It closes the db connection after running th query




## Database  Development
- I have used SQLite db approach to store the data extracted
- The code created a database named "normanpd.db" . For that i have used "CREATE TABLE IF NOT EXISTS". This will check if table exists or not. If no, it will create a new table with 5 coloumns as mentioned above. I have defined all coloumns as TEXT.
- I have used executemany() function of SQLite to insert multiple rows at once. The code makes sure that the db connection is committed and closed at appropiate times.
- I used Select statement to fetch the number of incidents nature-wise and display the results in the console

- The code basically follows a general database approach with creating table, inserting data and running queries on the table.SQLite engine made it a reliable and effiecnet for storing and fetching data.

## workflow of Database 
- The createdb() function creates a new db file(or opens an existing one) and creates "incidents" table . The funvtion then returns a conection to the database.

- Then populatedb() function takes that connection as input and populates the 'incidents' table with data using SQL query.

- Now, statusdb() takes the db connection object as input and runs 'Select' statement to fetch the count of incidents grouped by nature and displays the results.
- Overall , to use this script we call "fetchincidents(url)" to fetch incident data and passed the binary data to "extractincident(binary_data)" function to extract data. Then 'createdb()' creates the db file and table and pass db connection object and processes data to "populatedb()" to populate the data into database. At last we can the "status(db)" function to display the count of incidents grouped by nature.




## Test Functions

1. test_fetchincidents():  The test makes sure that the output is in bytes format and the output length is not null.

2. test_extractincidents():  This checks that output is of type list and the length of ouput from "extractincidents()" is greateror equal to 0. It also makes sure that every  inner list have exactly 5 elements in it.

3. test_createdb(): It checks that a table named incidents was actually created  in the database and the output of "createdb()" is not "none".

4. test_populatedb():This test function creates a database,then inserts data into it and at last checks thay data was correctly inserted into the database by checking the fields should match the expexted values.

5. test_status(): It uses the same approach as "test_populatedb()" function to create and populate db.It then redirects the output to StringIO object to check and capture the output of "status()" function.It checks that "status()" runs without any errors.


## Bugs and Assumptions
1. I have assumed the data in PDF is consistent,but in real world this might not be the case. Hence , inconsistency in the data can break the code and/or produce incorrect output.
2. The regular expression used to match data from PDF file may not always match. This can lead to incoorect output.
3. If the PDF file is encrypted or corrupted, the parsing(which is done using PyPDF2)  may fail and code will now give any output.
4. The code have assumed data to be complete.However, there might be a case of missing values. In such cases,the code may not produce exact desired outcome.

## how to run
<img src="(https://www.canva.com/design/DAFcptxbzVk/YDXMv2mvwXX1Z2kM50Wglw/watch)" alt="Gif VIdeo of code Running">


