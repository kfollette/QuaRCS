# Database Generation
The database generation subproject takes scored data in .csv format, creates the appropriate SQL statements, and uploads the data to the quarcs database.

If the database is still maintained on the Exoplanet computer in the Follette Lab, use that computer and skip to **Working with the Database** below.

## Installation
Download MySQL Community Server here: https://dev.mysql.com/downloads/mysql/

During this istallation, you will be prompted to setup a username and password.
  ```
  User: root
  Password: *********  
  ```
Then run:
```
pip install mysqlclient 
pip install mysql-connector-python
pip install csvkit   
pip install cs50
```
Install any additional modules if they are needed.

You may find it easier to interact with the database using MySQLWorkbench. It can be downloaded here: https://dev.mysql.com/downloads/workbench/

### Troubleshooting:
The mysql folder may not be on the same path as the database generation directory. To resolve temporarily:
```
export PATH=$PATH:/usr/local/mysql/bin
```
To resolve permanently:
```
echo 'export PATH="/usr/local/mysql/bin:$PATH"' >> ~/.bash_profile
```
Before running the script, sql_mode should be changed from the default to " ". This can be done by manually editing the relevant line in ```/usr/local/etc/my.cnf``` if it exists. Alternatively, log into mysql using the command line and run ```SET GLOBAL sql_mode = " "```;. This will change sql_mode for that session.

### Help for MySQLWorkbench:
Select the wrench icon next to INSTANCE in the sidebar

Manually input the configuration file as /usr/local/etc/my.cnf

If this file does not exist, download mysql using brew: ```brew install mysql```

Then confirm the existence of ```my.cnf``` using the command line and try again.

Alternatively, set the configuration file to ```my.cnf``` provided in this repository. 

# Working with the Database

The local database is maintained on the Exoplanet computer in the Follette lab. 

## Upload Public Data Locally:
Confirm all required setup and troubleshooting has been completed. Add all new semester data to the ```data``` folder in the same directory as the script. Then run:
```
python merge_data.py 
```

This will produce a merged .csv file named with the current date. Then run:
```
python masterscript.py filename
```

Do not include the .csv extention with filename. Additionally, make sure the file name for the data to upload is mysql compliant - it should not include spaces, dashes, or hashtags.

You can confirm that the server is running using MySQLWorkbench. You can manually check the data using ```SHOW TABLES FROM quarcs```; in mysql on the command line or in MySQLWorkbench.

(If the QuaRCS survey is updated to include new questions, new duplicate columns may appear in the .csv merged input data. This can be easily resolved by adding another data.replace() statement in ```script.py```.)

## Transfer Local Database to Website

