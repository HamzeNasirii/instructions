# Generated by Django 4.2.3 on 2023-08-07 14:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_delete_behvarz'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manager',
            name='user',
        ),
        migrations.DeleteModel(
            name='Expert',
        ),
        migrations.DeleteModel(
            name='Manager',
        ),
    ]