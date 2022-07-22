<img src="https://coveralls.io/repos/github/XValentavr/EPAMFlaskFinalProject/badge.svg" alt="Coverage Status" />
https://coveralls.io/github/XValentavr/EPAMFlaskFinalProject

# Hospital app

This is a web application for managing your financial. It uses a RESTful web service to perform crud operations. The app
allows you to:

- enter as superuser to get all privileges
- create/delete wallet and set it as general for all users
- create new user or delete existing user if current user is a superuser
- add money to any wallet and any currency
- delete entered transaction
- change entered transaction
- use search form to get history of transaction
- add money
- delete money
- pay using percents
- move money form wallet to wallet
- exchange money using currency and rate

## How to build

#### Clone the repo

```git@github.com:XValentavr/Financial.git```

or download as an archive

#### Install all the dependencies

```pip install -r requirements.txt```

#### Set up the database

MySql must be installed. Go to the mysql console, login as root and create a new user:  
```CREATE USER *user* IDENTIFIED BY *password*```  
Replace the \*user* and the \*password* with your own values

#### Set the environmental variables

For Windows:  
```set FLASK_APP=run.py```  
```set FLASK_CONFIG=*config*```   
```set SECRET_KEY=*secret_key*```  
```set DB_URL=mysql+pymysql://*user*:*password*@localhost/financialapp```  
For Linux:  
```export FLASK_APP=run.py```  
```export FLASK_CONFIG=*config*```
```export SECRET_KEY=*secret_key*```  
```export DB_URL=mysql+pymysql://*user*:*password*@localhost/financialapp```

Replace the \*config* with one of the values: *development*,
*production*, *testing*

Replace the \*key*, \*user* and the \*password* with your own values

#### Run the migration scripts to create database schema

Run the following commands:  
```flask db migrate```  
```flask db upgrade```

If you encounter some problems, remove the migration folder from project root and run the following commands:  
```flask db init```  
```flask db migrate```  
```flask db upgrade```

### Everything is ready! Run the app

To launch the app just run:  
```flask run```

## What you can do

### Here is the list of available addresses of web service:

#### Here is the list of available addresses of web application:

#### Finance

- /income - add money
- /outcome - withdraw money
- /pay - pay with percents
- /move - move from wallet to wallet
- /exchange - exchange money

#### Users

- /add - add new user
- /change - current user info
- /users/edit/<slug:uuid> - change user
- /delete - API to delete user

#### Login

- / or /login - login to app
- /logout - logout

#### Wallet

- /wallet - add new wallet and set general for some users
- /changewallet - information about wallet
- /wallet/edit/<slug:wallet> - edit current wallet
- /delete - delete current wallet