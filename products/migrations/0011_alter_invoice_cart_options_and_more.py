# Generated by Django 4.0.3 on 2022-04-08 23:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_rename_cart_invoice_cart_alter_product_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invoice_cart',
            options={'verbose_name_plural': 'Invoices Carts'},
        ),
        migrations.AlterField(
            model_name='invoice_cart',
            name='invoice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice_cart', to='products.invoice'),
        ),
    ]
