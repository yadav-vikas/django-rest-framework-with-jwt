# Generated by Django 4.0.5 on 2022-06-07 11:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='expense',
            options={'ordering': ['-date']},
        ),
    ]
