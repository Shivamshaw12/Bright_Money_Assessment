# Generated by Django 4.2.5 on 2023-09-27 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manageLoansApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='load_id',
            field=models.UUIDField(primary_key=True, serialize=False),
        ),
    ]