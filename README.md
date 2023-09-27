# Bright_Money_Assessment

Loan_Management_System
Bright-Money-Assignment

How to run this project locally

Clone this repo and install all dependencies
$ pip3 install -r requirements.txt

Note: if any confilct happen install them seperately
#Step 1: Migrate the models Create a migration for the models using the command:

>> python manage.py makemigrations

Then run the migration to create the necessary tables in the database using the command:

>> python manage.py migrate
#Step 2: Install and configure Celery and RabbitMQ Install Celery and RabbitMQ using the following commands:

>> pip install celery
>> sudo apt-get install rabbitmq-server

Configure Celery to use RabbitMQ as the message broker by adding the following code to the settings.py file:

>>CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'
>>CELERY_RESULT_BACKEND = 'rpc://'`
#Step 3: Start the Django server, Celery worker, and RabbitMQ server Start the Django server using the command:

>> python manage.py runserver

Start the Celery worker using the command:
>> celery -A loan_api_project worker -l info

Start the RabbitMQ server using the command:
>>rabbitmq-server
