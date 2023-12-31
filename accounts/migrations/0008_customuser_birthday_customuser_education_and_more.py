# Generated by Django 4.2.3 on 2023-07-31 06:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_remove_manager_date_employee_manager_is_manager'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='education',
            field=models.CharField(blank=True, choices=[('High school', 'High school'), ('Diploma', 'Diploma'), ('Associate Degree', 'Associate Degree'), ('Bachelor degree', 'Bachelor degree')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='gender',
            field=models.CharField(blank=True, choices=[('man', 'Man'), ('women', 'Women'), ('other', 'Other')], max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(blank=True, choices=[('manager', 'Manager'), ('expert', 'Expert'), ('behvarz', 'Behvarz')], max_length=7, null=True),
        ),
        migrations.AlterField(
            model_name='city',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='province_cities', to='accounts.province'),
        ),
        migrations.AlterField(
            model_name='healthcenter',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='city_healthCenter', to='accounts.city'),
        ),
        migrations.AlterField(
            model_name='village',
            name='health_center',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='health_village', to='accounts.healthcenter'),
        ),
    ]
