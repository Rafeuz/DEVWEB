# Generated by Django 2.2.4 on 2019-11-23 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Encomenda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('tipo', models.CharField(max_length=45)),
                ('descricao', models.TextField(max_length=500)),
                ('preco', models.DecimalField(decimal_places=2, max_digits=7)),
            ],
        ),
    ]