# Bright Money Assessment

# Loan Management App

Steps to run this project locally 

#Install all dependencies of this project
```sh
$ pip install -r requirements.txt

```

#Migrate the models:
```sh
>> python manage.py makemigrations

Then run:

>> python manage.py migrate
```

#Start the Django server:
```sh
>> python manage.py runserver

```
To apply migration from csv file to Django db run this command:
```sh
>> python manage.py runscript load_csv
```

# Configration for the apis are:

#POST api to register the user:
```sh
http://localhost:port/api/register-user/?aadhar_id=b7fa4071-5883-4ac6-830e-4bb5a4cd7826&name=shivam&email=mail@mail.com&annual_income=500000

#Parameters:
aadhar_id=b7fa4071-5883-4ac6-830e-4bb5a4cd7826 // used in transactions 
name=shivam
email=mail@mail.com
annual_income=500000
```

#POST api to apply for loan:
```sh
http://localhost:port/api/apply-loan/?unique_user_id=3&loan_type=Car&loan_amount=50000&interest_rate=12&term_period=11&disbursement_date=2020-01-24

#Parameters:
unique_user_id=3&loan_type=Car
loan_amount=50000
interest_rate=12
term_period=11
disbursement_date=2020-01-24
```

#GET api to get statement :
```sh
http://localhost:port/api/get-statement/?loan_id=e30fccf1-4c64-4ff8-b577-769c3d46b32e

#Parameters:
loan_id=e30fccf1-4c64-4ff8-b577-769c3d46b32e
```

#POST api to make payments to emis:
```sh
http://localhost:port/api/make-payment/?loan_id=840ee969-2fa8-42ba-b6ed-b8f94ae3c42d&amount=20000

#Parameters:
loan_id=840ee969-2fa8-42ba-b6ed-b8f94ae3c42d
amount=20000
```
