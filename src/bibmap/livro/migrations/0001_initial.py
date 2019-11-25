# Generated by Django 2.2.4 on 2019-11-18 04:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Livro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('isbn_10', models.CharField(max_length=10)),
                ('isbn_13', models.CharField(max_length=13)),
                ('editora', models.CharField(max_length=50)),
                ('capa', models.ImageField(upload_to='images/livros/')),
                ('genero', models.IntegerField(choices=[(0, 'Ação'), (1, 'Administração'), (2, 'Aventura'), (3, 'Arte'), (4, 'Artesanato'), (5, 'Autoajuda'), (6, 'Biografia'), (7, 'Ciência'), (8, 'Computação'), (9, 'Humor'), (10, 'Direito'), (11, 'Educação'), (12, 'Didático'), (13, 'Engenharia'), (14, 'Erótico'), (15, 'Esporte'), (16, 'Ficção'), (17, 'Gastronomia'), (18, 'História'), (19, 'Quadrinho'), (20, 'Infantil'), (21, 'Infantojuvenil'), (22, 'LGBTQI+'), (23, 'Literatura'), (24, 'Medicina'), (25, 'Policial'), (26, 'Religião'), (27, 'Romance'), (28, 'Saúde'), (29, 'Turismo'), (30, 'Linguagem')], default=0)),
                ('status', models.BooleanField(default=True)),
                ('autor', models.TextField()),
                ('resumo', models.TextField()),
                ('last_reseted_views', models.DateField(default=datetime.date(2000, 1, 1))),
                ('visualizacoes', models.IntegerField(default=0)),
            ],
        ),
    ]
