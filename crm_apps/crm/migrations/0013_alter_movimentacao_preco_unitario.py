# Generated by Django 5.1.7 on 2025-04-13 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0012_movimentacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimentacao',
            name='preco_unitario',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Preço unitário desta movimentação', max_digits=10, null=True),
        ),
    ]
