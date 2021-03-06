# Generated by Django 4.0.3 on 2022-05-19 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='nationality_id',
            field=models.CharField(max_length=10, unique=True, verbose_name='National ID'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='occupation',
            field=models.CharField(max_length=100, verbose_name='Occupation'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='salary',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Salary'),
        ),
    ]
