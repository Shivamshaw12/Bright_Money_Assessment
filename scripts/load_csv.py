from manageLoansApp.models import Transaction
import csv

def run():
    with open('csv_files/transactions_data.csv') as file:
        reader = csv.reader(file)
        next(reader)
        Transaction.objects.all().delete()
        for row in reader:
            print(row)
            transaction = Transaction(user=row[0],
                        date=row[1],
                        amount=row[3],
                        transaction_type = row[2])
            transaction.save()