# Generated by Django 4.2.3 on 2023-08-15 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_remove_manager_user_delete_expert_delete_manager'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='accounts/user_photos/'),
        ),
    ]
